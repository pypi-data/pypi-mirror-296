from datetime import datetime

from caplib.numerics import *
from caplib.market import *
from caplib.datetime import *
from caplib.analytics import *
from caplib.processrequest import process_request

#CreatePmParRateCurve
def create_pm_par_rate_curve(as_of_date, currency, curve_name, pillars, tag, save, location, mode):
    try:
        pillars = list()
        for pillar in pillars:
            pillars.append(dqCreateProtoPmParRateCurve_Pillar(str(pillar[0]), 
                                              to_instrument_type(str(pillar[1])), 
                                              to_period(str(pillar[2])), 
                                              float(pillar[3])))            
        par_curve = dqCreateProtoPmParRateCurve(create_date(as_of_date),
                                                currency,
                                                curve_name,
                                                pillars)
        return par_curve
    except Exception as e:
        return str(e)
    
 #PmYieldCurveBuilder
def pm_yield_curve_builder(as_of_date, 
                           par_curve, 
                           inst_template, 
                           discount_curve, 
                           spot_price, 
                           curve_type, 
                           interp_method, 
                           extrap_method, 
                           day_count, 
                           curve_name, 
                           jacobian, 
                           shift, 
                           finite_diff_method, 
                           threading_mode):
    try:        
        pb_input = dqCreateProtoPmYieldCurveBuildingInput(create_date(as_of_date),
                                                          par_curve,
                                                          discount_curve,
                                                          spot_price,
                                                          jacobian,
                                                          to_day_count_convention(day_count),
                                                          to_interp_method(interp_method),
                                                          to_extrap_method(extrap_method),
                                                          to_ir_yield_curve_type(curve_type),
                                                          inst_template,
                                                          curve_name,
                                                          shift,
                                                          to_finite_difference_method(finite_diff_method),
                                                          to_threading_mode(threading_mode))
        req_name = "PM_YIELD_CURVE_BUILDER"
        res_msg = process_request(req_name, pb_input.SerializeToString())   
        pb_output = PmYieldCurveBuildingOutput()
        pb_output.ParseFromString(res_msg)        
        if pb_output.success == False:
            raise Exception(pb_output.err_msg)      
        return pb_output.yield_curve  
    except Exception as e:
        return [str(e)]
    
#CreatePmMktConventions
def create_pm_mkt_conventions(atm_type,
                              short_delta_type,
                              long_delta_type,
                              short_delta_cutoff,
                              risk_reversal,
                              smile_quote_type):    
    return dqCreateProtoPmMarketConventions(to_atm_type(atm_type),
                                            to_delta_type(short_delta_type),
                                            to_delta_type(long_delta_type),
                                            to_period(short_delta_cutoff),
                                            to_risk_reversal(risk_reversal),
                                            to_smile_quote_type(smile_quote_type))


def create_pm_option_quote_matrix(underlying: str,
                                  terms: list,
                                  payoff_types: list,
                                  deltas: list,
                                  quotes: list):
    try:
        quote_matrix = create_option_quote_matrix(
            "OQVT_VOLATILITY",
            "OQTT_RELATIVE_TERM",
            "OQST_DELTA_STRIKE",
            "EUROPEAN",
            "SPOT_UNDERLYING_TYPE",
            terms,
            [],
            payoff_types,
            quotes,
            deltas,
            underlying)
        return quote_matrix
    except Exception as e:
        return str(e)
    
def pm_vol_surface_builder(as_of_date,
                           vol_surf_definition,
                               option_quote_matrix,
                               mkt_conventions,
                               spot_price,
                               discount_curve,
                               fwd_curve,
                               building_settings,
                               spot_template,
                               underlying,
                               vol_surf_name,
                               tag,
                               rtn_type,
                               save,
                               location, 
                               mode):
    try:
        pb_input = dqCreateProtoPmVolatilitySurfaceBuildingInput(create_date(as_of_date),
                                                                 vol_surf_definition,
                                                                 option_quote_matrix,
                                                                 spot_price,
                                                                 discount_curve,
                                                                 fwd_curve,
                                                                 building_settings,
                                                                 mkt_conventions,
                                                                 spot_template,
                                                                 underlying,
                                                                 vol_surf_name)
        req_name = "PM_VOLATILITY_SURFACE_BUILDER"
        res_msg = process_request(req_name, pb_input.SerializeToString())
        pb_output = PmVolatilitySurfaceBuildingOutput()
        pb_output.ParseFromString(res_msg)
        if pb_output.success == False:
            raise Exception(pb_output.err_msg)
        return pb_output.vol_surf
    except Exception as e:
        return str(e)
    
#CreateCmOptionQuoteMatrix
def create_cm_option_quote_matrix(exercise_type, underlying_type, term_dates, payoff_types, strikes, prices, underlying):
    try:
        quote_matrix = create_option_quote_matrix(
            "OQVT_PRICE",
            "OQTT_ABOSULTE_TERM",
            "OQST_ABOSULTE_STRIKE",
            exercise_type,
            underlying_type,
            [],
            term_dates,
            payoff_types,
            prices,
            strikes,
            underlying)
        return quote_matrix
    except Exception as e:
        return str(e)
    
#CmVolSurfaceBuilder
def cm_vol_surface_builder(as_of_date, smile_method, wing_strike_type, lower, upper, option_quote_matrix, underlying_prices, discount_curve, fwd_curve, building_settings, underlying, name, tag, rtn_type, save, location, mode):
    try:
        dt = datetime.now()
        pb_input = dqCreateProtoCmVolatilitySurfaceBuildingInput(create_date(as_of_date),
                                                                 create_volatility_surface_definition("", smile_method, "", "", "", "", "", wing_strike_type, lower, upper),
                                                                 option_quote_matrix,
                                                                 dqCreateProtoVector(underlying_prices),
                                                                 discount_curve,
                                                                 fwd_curve,
                                                                 create_vol_surf_build_settings(building_settings[0], building_settings[1]),
                                                                 underlying)
        req_name = "CM_VOLATILITY_SURFACE_BUILDER"
        res_msg = process_request(req_name, pb_input.SerializeToString())
        pb_output = CmVolatilitySurfaceBuildingOutput()
        pb_output.ParseFromString(res_msg)
        if pb_output.success == False:
            raise Exception(pb_output.err_msg)
        return pb_output.vol_surf
    except Exception as e:
        return str(e)



def create_cm_risk_settings(ir_curve_settings,
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
    return dqCreateProtoCmRiskSettings(ir_curve_settings,
                                       price_settings,
                                       vol_settings,
                                       price_vol_settings,
                                       theta_settings,
                                       dividend_curve_settings)

def create_cm_mkt_data_set(as_of_date: datetime,
                           discount_curve,
                           underlying_price,
                           vol_surf,
                           fwd_curve,
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
    return dqCreateProtoCmMktDataSet(create_date(as_of_date),
                                     discount_curve,
                                     fwd_curve,
                                     underlying_price,
                                     vol_surf,
                                     quanto_discount_curve,
                                     quanto_fx_vol_curve,
                                     quanto_correlation,
                                     underlying)

def run_cm_pricing(req_name, pb_input):

    pb_output = CmPricingOutput()
    res_msg = process_request(req_name, pb_input.SerializeToString())
    pb_output.ParseFromString(res_msg)
    if pb_output.success == False:
        raise Exception(pb_output.err_msg)
    return pb_output
 
#CmEuropeanOptionPricer
def cm_european_option_pricer(instrument, pricing_date, mkt_data_set, pricing_settings, risk_settings, scn_settings):
    pb_input = dqCreateProtoCmEuropeanOptionPricingInput(dqCreateProtoCmPricingInput(create_date(pricing_date), 
                                                                                     mkt_data_set, pricing_settings, risk_settings, 
                                                                                     False, '', '', '', '', '', 
                                                                                     scn_settings),
                                                         instrument)
    req_name = "CM_EUROPEAN_OPTION_PRICER"
    return run_cm_pricing(req_name,  pb_input.SerializeToString())

#CmAmericanOptionPricer
def cm_american_option_pricer(instrument, pricing_date, mkt_data_set, pricing_settings, risk_settings, scn_settings):
    try:
        pb_input = dqCreateProtoCmAmericanOptionPricingInput(dqCreateProtoCmPricingInput(create_date(pricing_date), 
                                                                                     mkt_data_set, pricing_settings, risk_settings, 
                                                                                     False, '', '', '', '', '', 
                                                                                     scn_settings),
                                                         instrument)
        req_name = "CM_AMERICAN_OPTION_PRICER"
        return run_cm_pricing(req_name,  pb_input.SerializeToString())        
    except Exception as e:
        return str(e)

#CmAsianOptionPricer
def cm_asian_option_pricer(instrument, pricing_date, mkt_data_set, pricing_settings, risk_settings, scn_settings):
    try:
        pb_input = dqCreateProtoCmAsianOptionPricingInput(dqCreateProtoCmPricingInput(create_date(pricing_date),
                                                                                     mkt_data_set, pricing_settings, risk_settings, 
                                                                                     False, '', '', '', '', '', 
                                                                                     scn_settings),
                                                         instrument)
        req_name = "CM_ASIAN_OPTION_PRICER"
        return run_cm_pricing(req_name,  pb_input.SerializeToString())        
    except Exception as e:
        return str(e)

#CmDigitalOptionPricer
def cm_digital_option_pricer(instrument, pricing_date, mkt_data_set, pricing_settings, risk_settings, scn_settings):
    try:
        pb_input = dqCreateProtoCmDigitalOptionPricingInput(dqCreateProtoCmPricingInput(create_date(pricing_date),
                                                                                     mkt_data_set, pricing_settings, risk_settings, 
                                                                                     False, '', '', '', '', '', 
                                                                                     scn_settings),
                                                         instrument)
        req_name = "CM_DIGITAL_OPTION_PRICER"
        return run_cm_pricing(req_name,  pb_input.SerializeToString())  
    except Exception as e:
        return str(e)

#CmSingleBarrierOptionPricer
def cm_single_barrier_option_pricer(instrument, pricing_date, mkt_data_set, pricing_settings, risk_settings, scn_settings):
    try:
        pb_input = dqCreateProtoCmSingleBarrierOptionPricingInput(dqCreateProtoCmPricingInput(create_date(pricing_date), 
                                                                                     mkt_data_set, pricing_settings, risk_settings, 
                                                                                     False, '', '', '', '', '', 
                                                                                     scn_settings),
                                                         instrument)
        req_name = "CM_SINGLE_BARRIER_OPTION_PRICER"
        return run_cm_pricing(req_name,  pb_input.SerializeToString())  
    except Exception as e:
        return str(e)
        
#CmDoubleBarrierOptionPricer
def cm_double_barrier_option_pricer(instrument, pricing_date, mkt_data_set, pricing_settings, risk_settings, scn_settings):
    try:
        pb_input = dqCreateProtoCmDoubleBarrierOptionPricingInput(dqCreateProtoCmPricingInput(create_date(pricing_date), 
                                                                                     mkt_data_set, pricing_settings, risk_settings, 
                                                                                     False, '', '', '', '', '', 
                                                                                     scn_settings),
                                                         instrument)
        req_name = "CM_DOUBLE_BARRIER_OPTION_PRICER"
        return run_cm_pricing(req_name,  pb_input.SerializeToString()) 
    except Exception as e:
        return str(e)

#CmOneTouchOptionPricer
def cm_one_touch_option_pricer(instrument, pricing_date, mkt_data_set, pricing_settings, risk_settings, scn_settings):
    try:
        pb_input = dqCreateProtoCmOneTouchOptionPricingInput(dqCreateProtoCmPricingInput(create_date(pricing_date), 
                                                                                     mkt_data_set, pricing_settings, risk_settings, 
                                                                                     False, '', '', '', '', '', 
                                                                                     scn_settings),
                                                         instrument)
        req_name = "CM_ONE_TOUCH_OPTION_PRICER"
        return run_cm_pricing(req_name,  pb_input.SerializeToString()) 
    except Exception as e:
        return str(e)

#CmDoubleTouchOptionPricer
def cm_double_touch_option_pricer(instrument, pricing_date, mkt_data_set, pricing_settings, risk_settings, scn_settings):
    try:
        pb_input = dqCreateProtoCmDoubleTouchOptionPricingInput(dqCreateProtoCmPricingInput(create_date(pricing_date), 
                                                                                     mkt_data_set, pricing_settings, risk_settings, 
                                                                                     False, '', '', '', '', '', 
                                                                                     scn_settings),
                                                         instrument)
        req_name = "CM_DOUBLE_TOUCH_OPTION_PRICER"
        return run_cm_pricing(req_name,  pb_input.SerializeToString())
    except Exception as e:
        return str(e)

#CmRangeAccrualOptionPricer
def cm_range_accrual_option_pricer(instrument, pricing_date, mkt_data_set, pricing_settings, risk_settings, scn_settings):
    try:
        pb_input = dqCreateProtoCmRangeAccrualOptionPricingInput(dqCreateProtoCmPricingInput(create_date(pricing_date), 
                                                                                     mkt_data_set, pricing_settings, risk_settings, 
                                                                                     False, '', '', '', '', '', 
                                                                                     scn_settings),
                                                         instrument)
        req_name = "CM_RANGE_ACCRUAL_OPTION_PRICER"
        return run_cm_pricing(req_name,  pb_input.SerializeToString())
    except Exception as e:
        return str(e)

#CmSingleSharkFinOptionPricer
def cm_single_shark_fin_option_pricer(instrument, pricing_date, mkt_data_set, pricing_settings, risk_settings, scn_settings):
    try:
        pb_input = dqCreateProtoCmSingleSharkFinOptionPricingInput(dqCreateProtoCmPricingInput(create_date(pricing_date),
                                                                                     mkt_data_set, pricing_settings, risk_settings, 
                                                                                     False, '', '', '', '', '', 
                                                                                     scn_settings),
                                                         instrument)
        req_name = "CM_SINGLE_SHARK_FIN_OPTION_PRICER"
        return run_cm_pricing(req_name,  pb_input.SerializeToString()) 
    except Exception as e:
        return str(e)

#CmDoubleSharkFinOptionPricer
def cm_double_shark_fin_option_pricer(instrument, pricing_date, mkt_data_set, pricing_settings, risk_settings, scn_settings):
    try:
        pb_input = dqCreateProtoCmDoubleSharkFinOptionPricingInput(dqCreateProtoCmPricingInput(create_date(pricing_date), 
                                                                                     mkt_data_set, pricing_settings, risk_settings, 
                                                                                     False, '', '', '', '', '', 
                                                                                     scn_settings),
                                                         instrument)
        req_name = "CM_DOUBLE_SHARK_FIN_OPTION_PRICER"
        return run_cm_pricing(req_name,  pb_input.SerializeToString()) 
    except Exception as e:
        return str(e)

#CmPingPongOptionPricer
def cm_ping_pong_option_pricer(instrument, pricing_date, mkt_data_set, pricing_settings, risk_settings, scn_settings):
    try:
        pb_input = dqCreateProtoCmPingPongOptionPricingInput(dqCreateProtoCmPricingInput(create_date(pricing_date), 
                                                                                     mkt_data_set, pricing_settings, risk_settings, 
                                                                                     False, '', '', '', '', '', 
                                                                                     scn_settings),
                                                         instrument)
        req_name = "CM_PING_PONG_OPTION_PRICER"
        return run_cm_pricing(req_name,  pb_input.SerializeToString()) 
    except Exception as e:
        return str(e)

#CmAiirbagOptionPricer
def cm_airbag_option_pricer(instrument, pricing_date, mkt_data_set, pricing_settings, risk_settings, scn_settings):
    try:
        pb_input = dqCreateProtoCmAirbagOptionPricingInput(dqCreateProtoCmPricingInput(create_date(pricing_date), 
                                                                                     mkt_data_set, pricing_settings, risk_settings, 
                                                                                     False, '', '', '', '', '', 
                                                                                     scn_settings),
                                                         instrument)
        req_name = "CM_AIRBAG_OPTION_PRICER"
        return run_cm_pricing(req_name,  pb_input.SerializeToString()) 
    except Exception as e:
        return str(e)

#CmSnowballAutoCallableNotePricer
def cm_snowball_auto_callable_note_pricer(instrument, pricing_date, mkt_data_set, pricing_settings, risk_settings, scn_settings):
    try:
        pb_input = dqCreateProtoCmSnowballAutoCallableNotePricingInput(dqCreateProtoCmPricingInput(create_date(pricing_date), 
                                                                                     mkt_data_set, pricing_settings, risk_settings, 
                                                                                     False, '', '', '', '', '', 
                                                                                     scn_settings),
                                                         instrument)
        req_name = "CM_SNOWBALL_AUTOCALLABLE_NOTE_PRICER"
        return run_cm_pricing(req_name,  pb_input.SerializeToString()) 
    except Exception as e:
        return str(e)

#CmPhoenixAutoCallableNotePricer
def cm_phoenix_auto_callable_note_pricer(instrument, pricing_date, mkt_data_set, pricing_settings, risk_settings, scn_settings):
    try:
        pb_input = dqCreateProtoCmPhoenixAutoCallableNotePricingInput(dqCreateProtoCmPricingInput(create_date(pricing_date), 
                                                                                     mkt_data_set, pricing_settings, risk_settings, 
                                                                                     False, '', '', '', '', '', 
                                                                                     scn_settings),
                                                         instrument)
        req_name = "CM_PHOENIX_AUTOCALLABLE_NOTE_PRICER"
        return run_cm_pricing(req_name,  pb_input.SerializeToString()) 
    except Exception as e:
        return str(e)
