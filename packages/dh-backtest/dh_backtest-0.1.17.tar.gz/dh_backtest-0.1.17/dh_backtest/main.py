'''
This is a template for how to make use of this package to run backtest on a strategy.
'''
import numpy as np
import pandas as pd
from termcolor import cprint
from models.data_classes import Underlying, IBBarSize, FutureTradingAccount
from models.remote_data import get_spot_future_ib
from backtest_engine import BacktestEngine


def generate_signal(df:pd.DataFrame, para_comb:dict) -> pd.DataFrame:
    '''
    this is custom function to generate signals based on the historical data.
    return the input dataframe with extra column ['calculation_col_1', 'calculation_col_2', 'signal'].
    '''

    df['sma_5'] = df['close'].rolling(window=5).mean()
    df['sma_20'] = df['close'].rolling(window=20).mean()
    df['signal'] = ''

    prev_index = None
    for index, row in df.iterrows():
        # step 1: check if signal is present
        ''' Strategy:
        1. signal buy at golden cross
        2. signal sell at death cross
        '''
        if row['sma_5'] == np.nan or row['sma_20'] == np.nan:
            continue
        if prev_index is None:
            prev_index = index
            continue
        sma_5_current = row['sma_5']
        sma_20_current = row['sma_20']
        sma_5_prev = df.loc[prev_index, 'sma_5']
        sma_20_prev = df.loc[prev_index, 'sma_20']

        is_signal_buy = (sma_5_current > sma_20_current) and (sma_5_prev < sma_20_prev )
        is_signal_sell = (sma_5_current < sma_20_current) and (sma_5_prev > sma_20_prev)

        if is_signal_buy: df.loc[index,'signal'] = 'buy'
        if is_signal_sell: df.loc[index,'signal'] = 'sell'

        prev_index = index
    return df


def action_on_signal(df, para_comb, trade_account) -> pd.DataFrame:
    '''
    this is custom function for traders to determine what to do with their custome signal.
    return the input dataframe with extra column ['action', 'logic', 't_price', 't_size', 'commission', 'pnl_action' 'acc_columns'].
    the action can be 'buy', 'sell', and 'close' only.
    logic is the reason for the action. suggestion:['buy on signal', 'sell on signal', 'close on signal', 'stop loss limit', 'target profit', 'force close', 'margin call']
    t_price is the price to execute the action.
    t_size is the size of the position to execute the action.
    commission is the commission to be charged for the action.
    pnl_action is the realized profit and loss due to the action.
    acc_columns is the columns recording the changes of the trading account.
    '''
    my_acc = trade_account

    for index, row in df.iterrows():
        # step 1: determine if it is time to open position
        ''' Strategy: 
        1. if signal is buy and current position long or zero, add a long position
        2. if signal is sell and current position short or zero, add a short position
        3. if the signal inicate different direction from current position, skep this step
        '''
        initial_margin_per_contract = row['close']* my_acc.contract_multiplier * my_acc.margin_rate
        is_signal_buy = row['signal'] == 'buy'
        is_signal_sell = row['signal'] == 'sell'
        if my_acc.bal_avialable > initial_margin_per_contract:
            if is_signal_buy and my_acc.position_size >= 0:
                commission = my_acc.open_position(1, row['close'])
                df.loc[index, 'action'] = 'buy'
                df.loc[index, 'logic'] = 'open'
                df.loc[index, 't_size'] = 1
                df.loc[index, 't_price'] = row['close']
                df.loc[index, 'commission'] = commission
                df.loc[index, 'pnl_action'] = -commission

            elif is_signal_sell and my_acc.position_size <= 0:
                commission = my_acc.open_position(-1, row['close'])
                df.loc[index, 'action'] = 'sell'
                df.loc[index, 'logic'] = 'open'
                df.loc[index, 't_size'] = -1
                df.loc[index, 't_price'] = row['close']
                df.loc[index, 'commission'] = commission
                df.loc[index, 'pnl_action'] = -commission

        else:
            pass


        # step 2: determine if it is time to close position
        ''' Strategy:
        1. when the position profit reach the target, close the position
        2. when the position loss reach the stop loss, close the position
        3. when the margin call, close the position -> this is handled in the mark_to_market function
        '''
        target_pnl  = para_comb['target_profit']
        stop_loss   = -para_comb['stop_loss']
        contract_pnl = 0
        if my_acc.position_size != 0:
            if my_acc.position_size > 0:
                contract_pnl = row['close'] - my_acc.position_price
            elif my_acc.position_size < 0:
                contract_pnl = my_acc.position_price - row['close']

            if contract_pnl >= target_pnl or contract_pnl <= stop_loss:
                # cprint(f"Closing position at {row['close']}, P/L: {contract_pnl}", 'yellow')
                # print(f'curren position size: {my_acc.position_size}, price: {my_acc.position_price}, mkt price: {row["close"]}')
                df.loc[index, 'action']     = 'close'
                df.loc[index, 'logic']      = 'reach profit target' if contract_pnl >= target_pnl else 'reach stop loss'
                df.loc[index, 't_size']     = - my_acc.position_size
                df.loc[index, 't_price']    = row['close']
                commission, pnl_realized    = my_acc.close_position(-my_acc.position_size, row['close'])
                df.loc[index, 'commission'] = commission
                df.loc[index, 'pnl_action'] = pnl_realized


        # step 3: update the account and record the action if any
        mtm_result =  my_acc.mark_to_market(row['close'])

        if mtm_result['signal'] == 'margin call':
            df.loc[index, 'action'] = mtm_result['action']
            if mtm_result['action'] == 'close':
                df.loc[index, 'logic'] = mtm_result['logic']
                df.loc[index, 'commission'] = mtm_result['commission']
                df.loc[index, 'pnl_action'] = mtm_result['pnl_realized']

        df.loc[index, 'pos_size']       = int(my_acc.position_size)
        df.loc[index, 'pos_price']      = float(my_acc.position_price)
        df.loc[index, 'pnl_unrealized'] = float(my_acc.pnl_unrealized)
        df.loc[index, 'nav']            = float(my_acc.bal_equity)
        df.loc[index, 'bal_cash']       = float(my_acc.bal_cash)
        df.loc[index, 'bal_avialable']  = float(my_acc.bal_avialable)
        df.loc[index, 'margin_initial'] = float(my_acc.margin_initial)
        df.loc[index, 'cap_usage']      = f'{my_acc.cap_usage:.2f}%'
    
    return df




if __name__ == "__main__":
    underlying = Underlying(
        symbol='HSI',
        exchange='HKFE',
        contract_type='FUT',
        barSizeSetting=IBBarSize.DAY_1,
        start_date='2023-12-01',
        end_date='2024-03-31',
    )

    para_dict = {
        'stop_loss'         : [20, 30],
        'target_profit'     : [60, 80],
    }

    engine = BacktestEngine(
        is_update_data      =False,
        is_rerun_backtest   =True,
        underlying          =underlying,
        para_dict           =para_dict,
        trade_account       =FutureTradingAccount(150_000),
        generate_signal     =generate_signal,
        action_on_signal    =action_on_signal,
        get_data_from_api   =get_spot_future_ib,
        folder_path         ='data/backtest',
    )

    engine.run_engine()

