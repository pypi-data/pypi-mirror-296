from datetime import datetime

from caplib.numerics import *
from caplib.market import *
from caplib.datetime import *
from caplib.analytics import *
from caplib.processrequest import process_request

def create_eq_risk_settings(ir_curve_settings,
                            price_settings,
                            vol_settings,
                            price_vol_settings,
                            dividend_curve_settings,                            
                            theta_settings):
    """

    Parameters
    ----------
    ir_curve_settings: IrCurveRiskSettings
    price_settings: PriceRiskSettings
    vol_settings: VolRiskSettings
    price_vol_settings: PriceVolRiskSettings
    theta_settings: ThetaRiskSettings

    Returns
    -------
    FxRiskSettings

    """
    return dqCreateProtoEqRiskSettings(ir_curve_settings,
                                       price_settings,
                                       vol_settings,
                                       price_vol_settings,
                                       theta_settings,
                                       dividend_curve_settings)

def create_eq_mkt_data_set(as_of_date: datetime,
                           discount_curve,
                           underlying_price,
                           vol_surf,
                           dividend_curve,
                           quanto_discount_curve,
                           quanto_fx_vol_curve,
                           quanto_correlation,
                           underlying: str = ''):
    """

    Parameters
    ----------
    as_of_date: Date
    domestic_discount_curve: IrYieldCurve
    foreign_discount_curve: IrYieldCurve
    spot: FxSpotRate
    vol_surf: VolatilitySurface

    Returns
    -------
    FxMktDataSet

    """
    return dqCreateProtoEqMktDataSet(create_date(as_of_date),
                                     discount_curve,
                                     dividend_curve,
                                     underlying_price,
                                     vol_surf,
                                     quanto_discount_curve,
                                     quanto_fx_vol_curve,
                                     quanto_correlation,
                                     underlying)

#BuildEqIndexDividendCurve
def build_eq_index_dividend_curve(as_of_date,
                                    term_dates,
                                    future_prices,
                                    call_price_matrix,
                                    put_price_matrix,
                                    strike_matrix,
                                    spot,
                                    discount_curve,
                                    name,
                                    tag,
                                    save,
                                    location,
                                    mode):
    try:
        p_call_price_matrix = [dqCreateProtoVector(row) for row in call_price_matrix]
        p_put_price_matrix = [dqCreateProtoVector(row) for row in put_price_matrix]
        p_strike_matrix = [dqCreateProtoVector(row) for row in strike_matrix]
        pb_input = dqCreateProtoEqIndexDividendCurveBuildingInput([create_date(d) for d in term_dates],
                                                                  p_call_price_matrix,
                                                                  p_put_price_matrix,
                                                                  p_strike_matrix,
                                                                  spot,
                                                                  discount_curve,
                                                                  dqCreateProtoVector(future_prices))
                                                                  
        req_name = "EQ_INDEX_DIVIDEND_CURVE_BUILDER"
        res_msg = process_request(req_name, pb_input.SerializeToString())   
        pb_output = EqIndexDividendCurveBuildingOutput()
        pb_output.ParseFromString(res_msg)        
        if pb_output.success == False:
            raise Exception(pb_output.err_msg)      
        return pb_output.DividendCurve        
    except Exception as e:
        return str(e)

#CreateEqOptionQuoteMatrix
def create_eq_option_quote_matrix(exercise_type: str,
                                  underlying_type: str,
                                  term_dates: list, 
                                  payoff_types: list, 
                                  option_prices: list,
                                  option_strikes: list, 
                                  underlying: str = ''):
    try:
        return create_option_quote_matrix(
            "OQVT_PRICE",
            "OQTT_ABOSULTE_TERM",
            "OQST_ABOSULTE_STRIKE",
            exercise_type,
            underlying_type,
            [],
            term_dates,
            payoff_types,
            option_prices,
            option_strikes,
            underlying)

    except Exception as e:
        return str(e)

#EqVolSurfaceBuilder
def eq_vol_surface_builder(as_of_date: int,
                              smile_method: str,
                              wing_strike_type: str,
                              lower: float,
                              upper: float,
                              option_quote_matrix: str,
                              underlying_prices: list,
                              discount_curve: str,
                              dividend_curve: str,
                              pricing_settings: str,
                              building_settings: list,
                              underlying: str,
                              tag: str,
                              rtn_type: int,
                              save: bool,
                              location: str,
                              mode: str):
    try:
        dt = datetime.now()

        p_vol_surf_defintion = create_volatility_surface_definition("", smile_method, "", "", "", "", "", wing_strike_type, lower, upper)
        p_building_settings = create_vol_surf_build_settings(building_settings[0], building_settings[1])
        pb_input = dqCreateProtoEqVolatilitySurfaceBuildingInput(create_date(as_of_date), 
                                                                 p_vol_surf_defintion,
                                                                 option_quote_matrix,
                                                                 dqCreateProtoVector(underlying_prices),
                                                                 discount_curve,
                                                                 dividend_curve,
                                                                 p_building_settings,
                                                                 pricing_settings,
                                                                 underlying)
        req_name = "EQ_VOLATILITY_SURFACE_BUILDER"
        res_msg = process_request(req_name, pb_input.SerializeToString())   
        pb_output = EqVolatilitySurfaceBuildingOutput()
        pb_output.ParseFromString(res_msg)        
        if pb_output.success == False:
            raise Exception(pb_output.err_msg)      
        return pb_output.VolatilitySurface 
    except Exception as e:
        return str(e)

def run_eq_pricing(req_name, pb_input):

    pb_output = EqPricingOutput()
    res_msg = process_request(req_name, pb_input.SerializeToString())
    pb_output.ParseFromString(res_msg)
    if pb_output.success == False:
        raise Exception(pb_output.err_msg)
    return pb_output
 
#EqEuropeanOptionPricer
def eq_european_option_pricer(instrument, pricing_date, mkt_data_set, pricing_settings, risk_settings, scn_settings):
    pb_input = dqCreateProtoEqEuropeanOptionPricingInput(dqCreateProtoEqPricingInput(create_date(pricing_date), 
                                                                                     mkt_data_set, pricing_settings, risk_settings, 
                                                                                     False, '', '', '', '', '', 
                                                                                     scn_settings),
                                                         instrument)
    req_name = "EQ_EUROPEAN_OPTION_PRICER"
    return run_eq_pricing(req_name,  pb_input.SerializeToString())

#EqAmericanOptionPricer
def eq_american_option_pricer(instrument, pricing_date, mkt_data_set, pricing_settings, risk_settings, scn_settings):
    try:
        pb_input = dqCreateProtoEqAmericanOptionPricingInput(dqCreateProtoEqPricingInput(create_date(pricing_date), 
                                                                                     mkt_data_set, pricing_settings, risk_settings, 
                                                                                     False, '', '', '', '', '', 
                                                                                     scn_settings),
                                                         instrument)
        req_name = "EQ_AMERICAN_OPTION_PRICER"
        return run_eq_pricing(req_name,  pb_input.SerializeToString())        
    except Exception as e:
        return str(e)

#EqAsianOptionPricer
def eq_asian_option_pricer(instrument, pricing_date, mkt_data_set, pricing_settings, risk_settings, scn_settings):
    try:
        pb_input = dqCreateProtoEqAsianOptionPricingInput(dqCreateProtoEqPricingInput(create_date(pricing_date),
                                                                                     mkt_data_set, pricing_settings, risk_settings, 
                                                                                     False, '', '', '', '', '', 
                                                                                     scn_settings),
                                                         instrument)
        req_name = "EQ_ASIAN_OPTION_PRICER"
        return run_eq_pricing(req_name,  pb_input.SerializeToString())        
    except Exception as e:
        return str(e)

#EqDigitalOptionPricer
def eq_digital_option_pricer(instrument, pricing_date, mkt_data_set, pricing_settings, risk_settings, scn_settings):
    try:
        pb_input = dqCreateProtoEqDigitalOptionPricingInput(dqCreateProtoEqPricingInput(create_date(pricing_date),
                                                                                     mkt_data_set, pricing_settings, risk_settings, 
                                                                                     False, '', '', '', '', '', 
                                                                                     scn_settings),
                                                         instrument)
        req_name = "EQ_DIGITAL_OPTION_PRICER"
        return run_eq_pricing(req_name,  pb_input.SerializeToString())  
    except Exception as e:
        return str(e)

#EqSingleBarrierOptionPricer
def eq_single_barrier_option_pricer(instrument, pricing_date, mkt_data_set, pricing_settings, risk_settings, scn_settings):
    try:
        pb_input = dqCreateProtoEqSingleBarrierOptionPricingInput(dqCreateProtoEqPricingInput(create_date(pricing_date), 
                                                                                     mkt_data_set, pricing_settings, risk_settings, 
                                                                                     False, '', '', '', '', '', 
                                                                                     scn_settings),
                                                         instrument)
        req_name = "EQ_SINGLE_BARRIER_OPTION_PRICER"
        return run_eq_pricing(req_name,  pb_input.SerializeToString())  
    except Exception as e:
        return str(e)
        
#EqDoubleBarrierOptionPricer
def eq_double_barrier_option_pricer(instrument, pricing_date, mkt_data_set, pricing_settings, risk_settings, scn_settings):
    try:
        pb_input = dqCreateProtoEqDoubleBarrierOptionPricingInput(dqCreateProtoEqPricingInput(create_date(pricing_date), 
                                                                                     mkt_data_set, pricing_settings, risk_settings, 
                                                                                     False, '', '', '', '', '', 
                                                                                     scn_settings),
                                                         instrument)
        req_name = "EQ_DOUBLE_BARRIER_OPTION_PRICER"
        return run_eq_pricing(req_name,  pb_input.SerializeToString()) 
    except Exception as e:
        return str(e)

#EqOneTouchOptionPricer
def eq_one_touch_option_pricer(instrument, pricing_date, mkt_data_set, pricing_settings, risk_settings, scn_settings):
    try:
        pb_input = dqCreateProtoEqOneTouchOptionPricingInput(dqCreateProtoEqPricingInput(create_date(pricing_date), 
                                                                                     mkt_data_set, pricing_settings, risk_settings, 
                                                                                     False, '', '', '', '', '', 
                                                                                     scn_settings),
                                                         instrument)
        req_name = "EQ_ONE_TOUCH_OPTION_PRICER"
        return run_eq_pricing(req_name,  pb_input.SerializeToString()) 
    except Exception as e:
        return str(e)

#EqDoubleTouchOptionPricer
def eq_double_touch_option_pricer(instrument, pricing_date, mkt_data_set, pricing_settings, risk_settings, scn_settings):
    try:
        pb_input = dqCreateProtoEqDoubleTouchOptionPricingInput(dqCreateProtoEqPricingInput(create_date(pricing_date), 
                                                                                     mkt_data_set, pricing_settings, risk_settings, 
                                                                                     False, '', '', '', '', '', 
                                                                                     scn_settings),
                                                         instrument)
        req_name = "EQ_DOUBLE_TOUCH_OPTION_PRICER"
        return run_eq_pricing(req_name,  pb_input.SerializeToString())
    except Exception as e:
        return str(e)

#EqRangeAccrualOptionPricer
def eq_range_accrual_option_pricer(instrument, pricing_date, mkt_data_set, pricing_settings, risk_settings, scn_settings):
    try:
        pb_input = dqCreateProtoEqRangeAccrualOptionPricingInput(dqCreateProtoEqPricingInput(create_date(pricing_date), 
                                                                                     mkt_data_set, pricing_settings, risk_settings, 
                                                                                     False, '', '', '', '', '', 
                                                                                     scn_settings),
                                                         instrument)
        req_name = "EQ_RANGE_ACCRUAL_OPTION_PRICER"
        return run_eq_pricing(req_name,  pb_input.SerializeToString())
    except Exception as e:
        return str(e)

#EqSingleSharkFinOptionPricer
def eq_single_shark_fin_option_pricer(instrument, pricing_date, mkt_data_set, pricing_settings, risk_settings, scn_settings):
    try:
        pb_input = dqCreateProtoEqSingleSharkFinOptionPricingInput(dqCreateProtoEqPricingInput(create_date(pricing_date),
                                                                                     mkt_data_set, pricing_settings, risk_settings, 
                                                                                     False, '', '', '', '', '', 
                                                                                     scn_settings),
                                                         instrument)
        req_name = "EQ_SINGLE_SHARK_FIN_OPTION_PRICER"
        return run_eq_pricing(req_name,  pb_input.SerializeToString()) 
    except Exception as e:
        return str(e)

#EqDoubleSharkFinOptionPricer
def eq_double_shark_fin_option_pricer(instrument, pricing_date, mkt_data_set, pricing_settings, risk_settings, scn_settings):
    try:
        pb_input = dqCreateProtoEqDoubleSharkFinOptionPricingInput(dqCreateProtoEqPricingInput(create_date(pricing_date), 
                                                                                     mkt_data_set, pricing_settings, risk_settings, 
                                                                                     False, '', '', '', '', '', 
                                                                                     scn_settings),
                                                         instrument)
        req_name = "EQ_DOUBLE_SHARK_FIN_OPTION_PRICER"
        return run_eq_pricing(req_name,  pb_input.SerializeToString()) 
    except Exception as e:
        return str(e)

#EqPingPongOptionPricer
def eq_ping_pong_option_pricer(instrument, pricing_date, mkt_data_set, pricing_settings, risk_settings, scn_settings):
    try:
        pb_input = dqCreateProtoEqPingPongOptionPricingInput(dqCreateProtoEqPricingInput(create_date(pricing_date), 
                                                                                     mkt_data_set, pricing_settings, risk_settings, 
                                                                                     False, '', '', '', '', '', 
                                                                                     scn_settings),
                                                         instrument)
        req_name = "EQ_PING_PONG_OPTION_PRICER"
        return run_eq_pricing(req_name,  pb_input.SerializeToString()) 
    except Exception as e:
        return str(e)

#EqAirbagOptionPricer
def eq_airbag_option_pricer(instrument, pricing_date, mkt_data_set, pricing_settings, risk_settings, scn_settings):
    try:
        pb_input = dqCreateProtoEqAirbagOptionPricingInput(dqCreateProtoEqPricingInput(create_date(pricing_date), 
                                                                                     mkt_data_set, pricing_settings, risk_settings, 
                                                                                     False, '', '', '', '', '', 
                                                                                     scn_settings),
                                                         instrument)
        req_name = "EQ_AIRBAG_OPTION_PRICER"
        return run_eq_pricing(req_name,  pb_input.SerializeToString()) 
        return run_eq_pricing(req_name,
                             pb_input.SerializeToString(),
                             instrument,
                             mode)
    except Exception as e:
        return str(e)

#EqSnowballAutoCallableNotePricer
def eq_snowball_auto_callable_note_pricer(instrument, pricing_date, mkt_data_set, pricing_settings, risk_settings, scn_settings):
    try:
        pb_input = dqCreateProtoEqSnowballAutoCallableNotePricingInput(dqCreateProtoEqPricingInput(create_date(pricing_date), 
                                                                                     mkt_data_set, pricing_settings, risk_settings, 
                                                                                     False, '', '', '', '', '', 
                                                                                     scn_settings),
                                                         instrument)
        req_name = "EQ_SNOWBALL_AUTOCALLABLE_NOTE_PRICER"
        return run_eq_pricing(req_name,  pb_input.SerializeToString()) 
    except Exception as e:
        return str(e)

#EqPhoenixAutoCallableNotePricer
def eq_phoenix_auto_callable_note_pricer(instrument, pricing_date, mkt_data_set, pricing_settings, risk_settings, scn_settings):
    try:
        pb_input = dqCreateProtoEqPhoenixAutoCallableNotePricingInput(dqCreateProtoEqPricingInput(create_date(pricing_date), 
                                                                                     mkt_data_set, pricing_settings, risk_settings, 
                                                                                     False, '', '', '', '', '', 
                                                                                     scn_settings),
                                                         instrument)
        req_name = "EQ_PHOENIX_AUTOCALLABLE_NOTE_PRICER"
    except Exception as e:
        return str(e)
