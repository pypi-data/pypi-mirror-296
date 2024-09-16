import math
from typing import Tuple
from db_hj3415.myredis import C101, C103, C104

import logging

logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(levelname)s: [%(name)s] %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.setLevel(logging.WARNING)


def set_data(*args) -> list:
    """
    비유효한 내용 제거(None,nan)하고 중복된 항목 제거하고 리스트로 반환한다.
    여기서 set의 의미는 집합을 뜻함
    :param args:
    :return:
    """
    return [i for i in {*args} if i != "" and i is not math.nan and i is not None]


def calc당기순이익(code: str) -> Tuple[str, float]:
    """지배지분 당기순이익 계산

    일반적인 경우로는 직전 지배주주지분 당기순이익을 찾아서 반환한다.\n
    금융기관의 경우는 지배당기순이익이 없기 때문에\n
    계산을 통해서 간접적으로 구한다.\n
    """
    logger.debug(f'In the calc당기순이익... code:{code}')
    c103q = C103(code, 'c103재무상태표q')
    try:
        # print("*(지배)당기순이익: ", c103q.latest_value_pop2('*(지배)당기순이익'))
        return c103q.latest_value_pop2('*(지배)당기순이익')
    except:
        logger.warning(f"{code} - (지배)당기순이익이 없는 종목. 수동으로 계산합니다(금융관련업종일 가능성있음).")
        c103q.page = 'c103손익계산서q'
        최근당기순이익date, 최근당기순이익value = c103q.sum_recent_4q('당기순이익')
        c103q.page = 'c103재무상태표q'
        비지배당기순이익date, 비지배당기순이익value = c103q.latest_value_pop2('*(비지배)당기순이익')

        # 가변리스트 언패킹으로 하나의 날짜만 사용하고 나머지는 버린다.
        date, *_ = set_data(최근당기순이익date, 비지배당기순이익date)
        계산된지배당기순이익value = 최근당기순이익value - 비지배당기순이익value

        return date, 계산된지배당기순이익value


def calc유동자산(code: str) -> Tuple[str, float]:
    """유효한 유동자산 계산

    일반적인 경우로 유동자산을 찾아서 반환한다.\n
    금융기관의 경우는 간접적으로 계산한다.\n
    Red와 Blue에서 사용한다.\n
    """
    logger.debug(f'In the calc유동자산... code:{code}')
    c103q = C103(code, 'c103재무상태표q')
    try:
        return c103q.sum_recent_4q('유동자산')
    except:
        logger.warning(f"{code} - 유동자산이 없는 종목. 수동으로 계산합니다(금융관련업종일 가능성있음).")
        d1, v1 = c103q.latest_value_pop2('현금및예치금')
        d2, v2 = c103q.latest_value_pop2('단기매매금융자산')
        d3, v3 = c103q.latest_value_pop2('매도가능금융자산')
        d4, v4 = c103q.latest_value_pop2('만기보유금융자산')
        logger.debug(f'현금및예치금 : {d1}, {v1}')
        logger.debug(f'단기매매금융자산 : {d2}, {v2}')
        logger.debug(f'매도가능금융자산 : {d3}, {v3}')
        logger.debug(f'만기보유금융자산 : {d4}, {v4}')

        date, *_ = set_data(d1, d2, d3, d4)
        계산된유동자산value = v1 + v2 + v3 + v4

        return date, 계산된유동자산value


def calc유동부채(code: str) -> Tuple[str, float]:
    """유효한 유동부채 계산

    일반적인 경우로 유동부채를 찾아서 반환한다.\n
    금융기관의 경우는 간접적으로 계산한다.\n
    Red와 Blue에서 사용한다.\n
    """
    logger.debug(f'In the calc유동부채... code:{code}')
    c103q = C103(code, 'c103재무상태표q')
    try:
        return c103q.sum_recent_4q('유동부채')
    except:
        logger.warning(f"{code} - 유동부채가 없는 종목. 수동으로 계산합니다(금융관련업종일 가능성있음).")
        d1, v1 = c103q.latest_value_pop2('당기손익인식(지정)금융부채')
        d2, v2 = c103q.latest_value_pop2('당기손익-공정가치측정금융부채')
        d3, v3 = c103q.latest_value_pop2('매도파생결합증권')
        d4, v4 = c103q.latest_value_pop2('단기매매금융부채')
        logger.debug(f'당기손익인식(지정)금융부채 : {d1}, {v1}')
        logger.debug(f'당기손익-공정가치측정금융부채 : {d2}, {v2}')
        logger.debug(f'매도파생결합증권 : {d3}, {v3}')
        logger.debug(f'단기매매금융부채 : {d4}, {v4}')

        date, *_ = set_data(d1, d2, d3, d4)
        계산된유동부채value = v1 + v2 + v3 + v4

        return date, 계산된유동부채value


def calc비유동부채(code: str) -> Tuple[str, float]:
    """유효한 비유동부채 계산

    일반적인 경우로 비유동부채를 찾아서 반환한다.\n
    금융기관의 경우는 간접적으로 계산한다.\n
    Red와 Blue에서 사용한다.\n
    """
    logger.debug(f'In the calc비유동부채... code:{code}')
    c103q = C103(code, 'c103재무상태표q')
    try:
        return c103q.sum_recent_4q('비유동부채')
    except:
        logger.warning(f"{code} - 비유동부채가 없는 종목. 수동으로 계산합니다(금융관련업종일 가능성있음).")
        # 보험관련업종은 예수부채가 없는대신 보험계약부채가 있다...
        d1, v1 = c103q.latest_value_pop2('예수부채')
        d2, v2 = c103q.latest_value_pop2('보험계약부채(책임준비금)')
        d3, v3 = c103q.latest_value_pop2('차입부채')
        d4, v4 = c103q.latest_value_pop2('기타부채')
        logger.debug(f'예수부채 : {d1}, {v1}')
        logger.debug(f'보험계약부채(책임준비금) : {d2}, {v2}')
        logger.debug(f'차입부채 : {d3}, {v3}')
        logger.debug(f'기타부채 : {d4}, {v4}')

        date, *_ = set_data(d1, d2, d3, d4)
        계산된비유동부채value = v1 + v2 + v3 + v4

        return date, 계산된비유동부채value


def calc유동비율(code: str, pop_count: int) -> Tuple[str, float]:
    """유동비율계산 - Blue에서 사용

    c104q에서 최근유동비율 찾아보고 유효하지 않거나 \n
    100이하인 경우에는수동으로 계산해서 다시 한번 평가해 본다.\n
    """
    logger.debug(f'In the calc유동비율... code:{code}')
    c104q = C104(code, 'c104q')
    유동비율date, 유동비율value = c104q.mymongo_c1034.latest_value('유동비율', pop_count=pop_count)
    logger.debug(f'{code} 유동비율 : {유동비율value}({유동비율date})')

    if math.isnan(유동비율value) or 유동비율value < 100:
        logger.warning('유동비율 is under 100 or nan..so we will recalculate..')
        유동자산date, 유동자산value = calc유동자산(code)
        유동부채date, 유동부채value = calc유동부채(code)

        c103q = C103(code, 'c103현금흐름표q')
        추정영업현금흐름date, 추정영업현금흐름value = c103q.sum_recent_4q('영업활동으로인한현금흐름')
        logger.debug(f'{code} 계산전 유동비율 : {유동비율value}({유동비율date})')

        계산된유동비율 = 0
        try:
            계산된유동비율 = round(((유동자산value + 추정영업현금흐름value) / 유동부채value) * 100, 2)
        except ZeroDivisionError:
            logger.debug(f'유동자산: {유동자산value} + 추정영업현금흐름: {추정영업현금흐름value} / 유동부채: {유동부채value}')
            계산된유동비율 = float('inf')
        finally:
            logger.debug(f'{code} 계산된 유동비율 : {계산된유동비율}')
            date, *_ = set_data(유동자산date, 유동부채date, 추정영업현금흐름date)
            return date, 계산된유동비율
    else:
        return 유동비율date, 유동비율value


"""
FCF는 “Free Cash Flow”의 약자로, 한국어로는 “자유 현금 흐름”이라고 합니다. FCF는 기업이 운영 활동을 통해 창출한 현금 중에서 영업 및 자본적 지출을
 제외하고 남은 현금을 의미합니다. 이는 기업의 재무 건전성을 평가하는 중요한 지표로 사용됩니다. 자유 현금 흐름은 기업이 부채를 상환하고, 배당금을 지급하며,
  추가적인 투자를 할 수 있는 자금을 나타냅니다.
  
FCF의 중요성

1.	재무 건전성 평가: FCF는 기업이 실제로 얼마나 많은 현금을 창출하고 있는지를 보여줍니다. 이는 기업의 재무 건전성을 평가하는 데 중요한 지표입니다.
2.	투자 결정: 투자자들은 FCF를 통해 기업의 성장 가능성을 평가하고, 투자 결정을 내리는 데 참고합니다.
3.	배당 지급 능력: FCF는 기업이 주주들에게 배당금을 지급할 수 있는 능력을 나타냅니다.
4.	부채 상환: 기업은 FCF를 이용해 부채를 상환하고, 재무 구조를 개선할 수 있습니다.

CAPEX는 “Capital Expenditures”의 약자로, 한국어로는 “자본적 지출”이라고 합니다. CAPEX는 기업이 장기 자산을 구입하거나 유지하는 데 사용하는 
비용을 의미합니다. 이는 기업이 장기적인 성장을 위해 자산을 확장, 업그레이드 또는 유지하는 데 필요한 비용입니다. 이러한 자산에는 부동산, 건물, 기계,
 장비 등이 포함됩니다.
 
 CAPEX가 거의 없거나 아예 없는 업종에서도 자유 현금 흐름(Free Cash Flow, FCF)을 계산할 수 있습니다. CAPEX가 없는 경우,
  계산식에서 CAPEX 부분을 0으로 처리하면 됩니다.
"""


def findFCF(code: str) -> dict:
    """
    FCF 계산
    Returns:
        dict: 계산된 fcf 딕셔너리 또는 영업현금흐름 없는 경우 - {}

    Note:
        CAPEX 가 없는 업종은 영업활동현금흐름을 그대로 사용한다.\n

    """
    c103y = C103(code, 'c103현금흐름표y')
    _, 영업활동현금흐름_dict = c103y.find_without_yoy('영업활동으로인한현금흐름')
    c103y.page = 'c103재무상태표y'
    _, capex = c103y.find_without_yoy('*CAPEX')

    logger.debug(f'영업활동현금흐름 {영업활동현금흐름_dict}')
    logger.debug(f'CAPEX {capex}')

    if len(영업활동현금흐름_dict) == 0:
        return {}

    if len(capex) == 0:
        # CAPEX 가 없는 업종은 영업활동현금흐름을 그대로 사용한다.
        logger.warning(f"{code} - CAPEX가 없는 업종으로 영업현금흐름을 그대로 사용합니다..")
        return 영업활동현금흐름_dict

    # 영업 활동으로 인한 현금 흐름에서 CAPEX 를 각 연도별로 빼주어 fcf 를 구하고 리턴값으로 fcf 딕셔너리를 반환한다.
    r_dict = {}
    for i in range(len(영업활동현금흐름_dict)):
        # 영업활동현금흐름에서 아이템을 하나씩 꺼내서 CAPEX 전체와 비교하여 같으면 차를 구해서 r_dict 에 추가한다.
        영업활동현금흐름date, 영업활동현금흐름value = 영업활동현금흐름_dict.popitem()
        # 해당 연도의 capex 가 없는 경우도 있어 일단 capex를 0으로 치고 먼저 추가한다.
        r_dict[영업활동현금흐름date] = 영업활동현금흐름value
        for CAPEXdate, CAPEXvalue in capex.items():
            if 영업활동현금흐름date == CAPEXdate:
                r_dict[영업활동현금흐름date] = round(영업활동현금흐름value - CAPEXvalue, 2)
    logger.debug(f'r_dict {r_dict}')
    # 연도순으로 정렬해서 딕셔너리로 반환한다.
    return dict(sorted(r_dict.items(), reverse=False))


"""
PFCF의 중요성
1.	기업 가치 평가: PFCF는 기업이 창출하는 현금 흐름에 비해 주가가 적정한지 평가하는 데 사용됩니다. 낮은 PFCF는 주가가 상대적으로 저평가되었음을 나타낼
 수 있고, 높은 PFCF는 주가가 상대적으로 고평가되었음을 나타낼 수 있습니다.
2.	투자 결정: 투자자들은 PFCF를 사용하여 현금 흐름 창출 능력 대비 주가가 매력적인지를 판단하고, 투자 결정을 내리는 데 참고합니다.
3.	비교 분석: 같은 산업 내 다른 기업들과 비교하여, 어느 기업이 더 효율적으로 현금 흐름을 창출하는지를 평가할 수 있습니다.

PFCF의 한계

•산업 특성: PFCF는 산업마다 적정한 수준이 다를 수 있습니다. 예를 들어, 기술 산업과 제조 산업의 적정 PFCF는 다를 수 있습니다.
•일회성 항목: 특정 연도의 일회성 비용이나 수익이 FCF에 영향을 미칠 수 있으며, 이는 PFCF 계산에 왜곡을 가져올 수 있습니다.
"""


def findPFCF(code: str) -> dict:
    """Price to Free Cash Flow Ratio(주가 대비 자유 현금 흐름 비율)계산

    PFCF = 시가총액 / FCF

    Note:
        https://www.investopedia.com/terms/p/pricetofreecashflow.asp
    """
    # marketcap 계산 (fcf가 억 단위라 시가총액을 억으로 나눠서 단위를 맞춰 준다)
    marketcap억 = get_marketcap(code) / 100000000
    if math.isnan(marketcap억):
        return {}

    # pfcf 계산
    fcf_dict = findFCF(code)
    logger.debug(f'fcf_dict : {fcf_dict}')
    pfcf_dict = {}
    for FCFdate, FCFvalue in fcf_dict.items():
        if FCFvalue == 0:
            pfcf_dict[FCFdate] = math.nan
        else:
            pfcf_dict[FCFdate] = round(marketcap억 / FCFvalue, 2)
    logger.debug(f'pfcf_dict : {pfcf_dict}')
    return pfcf_dict


def get_marketcap(code: str) -> float:
    """
    시가총액(원) 반환
    :param code:
    :return:
    """
    c101 = C101(code)
    try:
        return int(c101.get_recent()['시가총액'])
    except KeyError:
        return math.nan
