from datetime import datetime

from caplib.numerics import *
from caplib.market import *
from caplib.datetime import *
from caplib.analytics import *
from caplib.processrequest import process_request

#NumericalFix
def to_numerical_fix(src):
    if src is None:
        return NONE_FIX
    
    if src in ['', 'nan']:
        return NONE_FIX
    else:
        return NumericalFix.DESCRIPTOR.values_by_name[src.upper()].number
    
#AccrualBias
def to_accrual_bias(src):
    if src is None:
        return HALFDAYBIAS
    
    if src in ['', 'nan']:
        return HALFDAYBIAS
    else:
        return AccrualBias.DESCRIPTOR.values_by_name[src.upper()].number
    
#ForwardsInCouponPeriod
def to_forwards_in_coupon_period(src):
    if src is None:
        return FLAT
    
    if src in ['', 'nan']:
        return FLAT
    else:
        return ForwardsInCouponPeriod.DESCRIPTOR.values_by_name[src.upper()].number
    
#CreateCrRiskSettings
def create_cr_risk_settings(ir_curve_settings, cs_curve_settings, theta_settings):
    settings = dqCreateProtoCrRiskSettings(ir_curve_settings,
                                           cs_curve_settings,
                                           theta_settings)
    return settings

#CreateCreditParCurve
def create_credit_par_curve(as_of_date, currency, name, pillars, tag, mode, save, location):
    try:
        pillars = list()
        for pillar in pillars:
            pillars.append(dqCreateProtoCreditParCurve_Pillar(str(pillar[0]), 
                                              to_instrument_type(str(pillar[1])), 
                                              to_period(str(pillar[2])), 
                                              float(pillar[3]), 
                                              to_instrument_start_convention('spot_start')))            
        pb_input = dqCreateProtoCreateCreditParCurveInput(create_date(as_of_date),
                                                          currency,
                                                          pillars,
                                                          name)
        req_name = "CREATE_CREDIT_PAR_CURVE"
        res_msg = process_request(req_name, pb_input.SerializeToString())   
        pb_output = CreateCreditParCurveOutput()
        pb_output.ParseFromString(res_msg)        
        if pb_output.success == False:
            raise Exception(pb_output.err_msg)      
        return pb_output.par_curve  
    except Exception as e:
        return str(e)
    
def credit_curve_builder(as_of_date, curve_name, build_settings, par_curve, discount_curve, building_method, calc_jacobian):
    try:
        pb_input = dqCreateProtoCreditCurveBuildingInput(par_curve,
                                                         curve_name,
                                                         create_date(as_of_date),
                                                         discount_curve,
                                                         building_method)        
        
        req_name = "CREDIT_CURVE_BUILDER"
        res_msg = process_request(req_name, pb_input.SerializeToString())   
        pb_output = CreditCurveBuildingOutput()
        pb_output.ParseFromString(res_msg)        
        if pb_output.success == False:
            raise Exception(pb_output.err_msg)      
        return pb_output.credit_curve  
    except Exception as e:
        return str(e)

#CreateCdsPricingSettings
def create_cds_pricing_settings(pricing_currency,
                                include_current_flow,
                                  cash_flows,
                                  include_settlement_flow,
                                  numerical_fix,
                                  accrual_bias,
                                  fwds_in_cpn_period,
                                  name,
                                  tag):
    try:
        model_params = [int(include_current_flow), 
                        int(to_numerical_fix(numerical_fix)), 
                        int(to_accrual_bias(accrual_bias)), 
                        int(to_forwards_in_coupon_period(fwds_in_cpn_period)) ]
        model_settings = create_model_settings("", model_params)
        settings = create_pricing_settings(
            pricing_currency,
            include_current_flow,
            cash_flows,
            None
        )
        settings.model_settings = model_settings
        return settings
    except Exception as e:
        return str(e)
    
#CreateCrMktDataSet
def dq_create_cr_fut_mkt_data_set(as_of_date, discount_curve, credit_curve, name, tag):
    try:
        mkt_data = dqCreateProtoCrMktDataSet(create_date(as_of_date),
                                             discount_curve,
                                             credit_curve)
        return mkt_data
    except Exception as e:
        return str(e)
    
#CreditDefaultSwapPricer
def credit_default_swap_pricer(instrument,
                                  pricing_date,
                                  mkt_data_set,
                                  pricing_settings,
                                  risk_settings,
                                  result_tag,
                                  rtn_type,
                                  mode):
    try:
        dt = datetime.now()
        credit_default_swap_pricing_input = dqCreateProtoCreditDefaultSwapPricingInput(create_date(pricing_date),
                                                                                       instrument,
                                                                                       mkt_data_set,
                                                                                       pricing_settings,
                                                                                       risk_settings,
                                                                                       False, '', '', '', '')
        req_name = "CREDIT_DEFAULT_SWAP_PRICER"
        res_msg = process_request(req_name, credit_default_swap_pricing_input.SerializeToString())   
        pb_output = CreditDefaultSwapPricingOutput()
        pb_output.ParseFromString(res_msg)        
        if pb_output.success == False:
            raise Exception(pb_output.err_msg)      
        return pb_output
    except Exception as e:
        return str(e)