"""red, mil, blue 3가지 분야에서 자료를 계산하여 리턴하는 함수 모음
"""
import math

from analyser_hj3415 import tools
from utils_hj3415 import utils
from db_hj3415 import myredis

import logging

logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(levelname)s: [%(name)s] %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.setLevel(logging.WARNING)


def red(code: str) -> dict:
    """
    리턴값
    {
        'red_price': red_price,
        '사업가치': 사업가치,
        '재산가치': 재산가치,
        '부채평가': 부채평가,
        '발행주식수': 발행주식수,
        'date': [각 유효한 값의 년월값 리스트(ex- 2020/09)],
    }
    """
    c103q = myredis.C103(code, 'c103재무상태표q')

    d1, 지배주주당기순이익 = tools.calc당기순이익(code)
    # print("지배주주당기순이익: ", 지배주주당기순이익)
    d2, 유동자산 = tools.calc유동자산(code)
    d3, 유동부채 = tools.calc유동부채(code)
    d4, 부채평가 = tools.calc비유동부채(code)

    c103q.page = 'c103재무상태표q'
    d5, 투자자산 = c103q.latest_value_pop2('투자자산')
    d6, 투자부동산 = c103q.latest_value_pop2('투자부동산')

    # 사업가치 계산 - 지배주주지분 당기순이익 / 기대수익률
    from analyser_hj3415 import cli
    EXPECT_EARN = utils.to_float(cli.AnalyserSettingsManager(cli.SETTINGS_FILE).get_value('EXPECT_EARN'))
    print('EXPECT_EARN', EXPECT_EARN)
    사업가치 = round(utils.nan_to_zero(지배주주당기순이익) / EXPECT_EARN, 2)

    # 재산가치 계산 - 유동자산 - (유동부채*1.2) + 고정자산중 투자자산
    재산가치 = round(유동자산 - (유동부채 * 1.2) + utils.nan_to_zero(투자자산) + utils.nan_to_zero(투자부동산), 2)

    _, 발행주식수 = c103q.latest_value_pop2('발행주식수')
    if math.isnan(발행주식수):
        발행주식수 = utils.to_int(myredis.C101(code).get_recent().get('발행주식'))
    else:
        발행주식수 = 발행주식수 * 1000

    try:
        red_price = round(((사업가치 + 재산가치 - 부채평가) * 100000000) / 발행주식수)
    except (ZeroDivisionError, ValueError) as e:
        red_price = math.nan

    logger.debug(f'Red Price : {red_price}원')
    return {
        'red_price': red_price,
        '지배주주당기순이익': 지배주주당기순이익,
        '사업가치': 사업가치,
        '유동자산': 유동자산,
        '유동부채': 유동부채,
        '투자자산': 투자자산,
        '투자부동산': 투자부동산,
        '재산가치': 재산가치,
        '부채평가': 부채평가,
        '발행주식수': 발행주식수,
        'EXPECT_EARN': EXPECT_EARN,
        'date': tools.set_data(d1, d2, d3, d4, d5, d6),  # ''값을 제거하고 리스트로 바꾼다.
    }


def mil(code: str) -> dict:
    """
    리턴값
    {
        '주주수익률': 주주수익률,
        '이익지표': 이익지표,
        '투자수익률': {'ROIC': roic, 'ROE': roe , 'ROE106': {}},
        '가치지표': {'FCF': fcf_dict, 'PFCF': pfcf_dict, 'PCR': pcr_dict},
        'date': [각 유효한 값의 년월값 리스트(ex- 2020/09)],
    }

    - 재무활동현금흐름이 마이너스라는 것은 배당급 지급했거나, 자사주 매입했거나, 부채를 상환한 상태임.
    - 반대는 채권자로 자금을 조달했거나 신주를 발행했다는 의미
    <주주수익률> - 재무활동현금흐름/시가총액 => 5%이상인가?

    투하자본수익률(ROIC)가 30%이상인가
    ROE(자기자본이익률) 20%이상이면 아주 우수 다른 투자이익률과 비교해볼것 10%미만이면 별로...단, 부채비율을 확인해야함.

    이익지표 ...영업현금흐름이 순이익보다 많은가 - 결과값이 음수인가..

    FCF는 영업현금흐름에서 자본적 지출(유·무형투자 비용)을 차감한 순수한 현금력이라 할 수 있다.
    말 그대로 자유롭게(Free) 사용할 수 있는 여윳돈을 뜻한다.
    잉여현금흐름이 플러스라면 미래의 투자나 채무상환에 쓸 재원이 늘어난 것이다.
    CAPEX(Capital expenditures)는 미래의 이윤을 창출하기 위해 지출된 비용을 말한다.
    이는 기업이 고정자산을 구매하거나, 유효수명이 당회계년도를 초과하는 기존의 고정자산에 대한 투자에 돈이 사용될 때 발생한다.

    잉여현금흐름이 마이너스일때는 설비투자가 많은 시기라 주가가 약세이며 이후 설비투자 마무리되면서 주가가 상승할수 있다.
    주가는 잉여현금흐름이 증가할때 상승하는 경향이 있다.
    fcf = 영업현금흐름 - capex

    가치지표평가
    price to fcf 계산
    https://www.investopedia.com/terms/p/pricetofreecashflow.asp
    pcr보다 정확하게 주식의 가치를 평가할수 있음. 10배이하 추천
    """
    c103q = myredis.C103(code, 'c103현금흐름표q')
    c104q = myredis.C104(code, 'c104q')
    c106q = myredis.C106(code, 'c106q')

    marketcap억 = tools.get_marketcap(code) / 100000000
    logger.debug(f'{code} market cap: {marketcap억}')
    fcf_dict = tools.findFCF(code)
    pfcf_dict = tools.findPFCF(code)
    d1, 지배주주당기순이익 = tools.calc당기순이익(code)

    d2, 재무활동현금흐름 = c103q.sum_recent_4q('재무활동으로인한현금흐름')
    d3, 영업활동현금흐름 = c103q.sum_recent_4q('영업활동으로인한현금흐름')

    d4, roic = c104q.sum_recent_4q('ROIC')
    d5, roe = c104q.latest_value_pop2('ROE')
    roe106 = c106q.find('ROE')

    _, pcr_dict = c104q.find_without_yoy('PCR')

    try:
        주주수익률 = round((재무활동현금흐름 / marketcap억 * -100), 2)
        이익지표 = round((지배주주당기순이익 - 영업활동현금흐름) / marketcap억, 5)
    except ZeroDivisionError:
        주주수익률 = math.nan
        이익지표 = math.nan

    if math.isnan(주주수익률) or math.isnan(이익지표):
        logger.warning(f'주주수익률: {주주수익률} 이익지표: {이익지표}')
        logger.warning(f'재무활동현금흐름: {재무활동현금흐름} / 지배주주당기순이익: {지배주주당기순이익} / 영업활동현금흐름: {영업활동현금흐름}')

    logger.debug(f'{code} fcf_dict : {fcf_dict}')
    logger.debug(f"{code} market_cap : {marketcap억}")
    logger.debug(f'{code} pfcf_dict : {pfcf_dict}')
    logger.debug(f'{code} pcr_dict : {pcr_dict}')

    return {
        '주주수익률': 주주수익률,
        '이익지표': 이익지표,
        '투자수익률': {'ROIC': roic, 'ROE': roe, 'ROE106': roe106},
        '가치지표': {'FCF': fcf_dict, 'PFCF': pfcf_dict, 'PCR': pcr_dict},
        'date': tools.set_data(d1, d2, d3, d4, d5),
    }


def blue(code: str) -> dict:
    """
    리턴값
    {
    'date': [각 유효한 값의 최근분기 값 리스트(ex- 2020/09)],
    '순부채비율': (29.99, {'2018/12': 19.45, '2019/12': 19.52, '2020/12': 12.07, '2021/12': 82.2, '2022/12': 29.99, '2023/12': nan}),
    '순운전자본회전율': (1.04, {'2018/12': 21.91, '2019/12': 23.12, '2020/12': 5.88, '2021/12': 5.6, '2022/12': 6.04, '2023/12': nan}),
    '유동비율': 64.29,
    '이자보상배율': (-3.64, {'2018/12': 4.01, '2019/12': 1.3, '2020/12': -5.05, '2021/12': 0.56, '2022/12': -1.28, '2023/12': nan}),
    '재고자산회전율': (1.66, {'2018/12': 12.41, '2019/12': 12.44, '2020/12': 9.18, '2021/12': 9.76, '2022/12': 8.79, '2023/12': nan})
    }

    <유동비율>
    100미만이면 주의하나 현금흐름창출력이 좋으면 괜찮을수 있다.
    만약 100%이하면 유동자산에 추정영업현금흐름을 더해서 다시계산해보아 기회를 준다.
    <이자보상배율>
    이자보상배율 영업이익/이자비용으로 1이면 자금사정빡빡 5이상이면 양호
    <순운전자금회전율>
    순운전자금 => 기업활동을 하기 위해 필요한 자금 (매출채권 + 재고자산 - 매입채무)
    순운전자본회전율은 매출액/순운전자본으로 일정비율이 유지되는것이 좋으며 너무 작아지면 순운전자본이 많아졌다는 의미로 재고나 외상이 쌓인다는 뜻
    <재고자산회전율>
    재고자산회전율은 매출액/재고자산으로 회전율이 낮을수록 재고가 많다는 이야기이므로 불리 전년도등과 비교해서 큰차이 발생하면 알람.
    재고자산회전율이 작아지면 재고가 쌓인다는뜻
    <순부채비율>
    부채비율은 업종마다 달라 일괄비교 어려우나 순부채 비율이 20%이하인것이 좋고 꾸준히 늘어나지 않는것이 좋다.
    순부채 비율이 30%이상이면 좋치 않다.
    <매출액>
    매출액은 어떤경우에도 성장하는 기업이 좋다.매출이 20%씩 늘어나는 종목은 유망한 종목
    <영업이익률>
    영업이익률은 기업의 경쟁력척도로 경쟁사에 비해 높으면 경제적해자를 갖춘셈
    """

    d1, 유동비율 = tools.calc유동비율(code, pop_count=3)
    logger.debug(f'유동비율 {유동비율} / [{d1}]')

    c104y = myredis.C104(code, 'c104y')
    _, dict이자보상배율y = c104y.find_with_yoy('이자보상배율')
    _, dict순운전자본회전율y = c104y.find_with_yoy('순운전자본회전율')
    _, dict재고자산회전율y = c104y.find_with_yoy('재고자산회전율')
    _, dict순부채비율y = c104y.find_with_yoy('순부채비율')

    c104q = myredis.C104(code, 'c104q')
    d6, 이자보상배율q = c104q.latest_value_pop2('이자보상배율')
    d7, 순운전자본회전율q = c104q.latest_value_pop2('순운전자본회전율')
    d8, 재고자산회전율q = c104q.latest_value_pop2('재고자산회전율')
    d9, 순부채비율q = c104q.latest_value_pop2('순부채비율')

    if len(dict이자보상배율y) == 0:
        logger.warning(f'empty dict - 이자보상배율 : {이자보상배율q} {dict이자보상배율y}')

    if len(dict순운전자본회전율y) == 0:
        logger.warning(f'empty dict - 순운전자본회전율 : {순운전자본회전율q} {dict순운전자본회전율y}')

    if len(dict재고자산회전율y) == 0:
        logger.warning(f'empty dict - 재고자산회전율 : {재고자산회전율q} {dict재고자산회전율y}')

    if len(dict순부채비율y) == 0:
        logger.warning(f'empty dict - 순부채비율 : {순부채비율q} {dict순부채비율y}')

    ################################################################

    return {
        '유동비율': 유동비율,
        '이자보상배율': (이자보상배율q, dict이자보상배율y),
        '순운전자본회전율': (순운전자본회전율q, dict순운전자본회전율y),
        '재고자산회전율': (재고자산회전율q, dict재고자산회전율y),
        '순부채비율': (순부채비율q, dict순부채비율y),
        'date': tools.set_data(d1, d6, d7, d8, d9),  # ''값을 제거하고 리스트로 바꾼다.
    }


def growth(code: str) -> dict:
    """
    리턴값
    {'date': [각 유효한 값의 최근분기 값 리스트(ex- 2020/09)],
    '매출액증가율': (-14.37, {'2018/12': -24.56, '2019/12': -20.19, '2020/12': -12.64, '2021/12': 38.65, '2022/12': -8.56, '2023/12': nan}),
    '영업이익률': {'뉴프렉스': '17.36', '동일기연': '13.58', '비에이치': '16.23', '에이엔피': '-9.30', '이브이첨단소재': '-4.93'}}

    <매출액>
    매출액은 어떤경우에도 성장하는 기업이 좋다.매출이 20%씩 늘어나는 종목은 유망한 종목
    <영업이익률>
    영업이익률은 기업의 경쟁력척도로 경쟁사에 비해 높으면 경제적해자를 갖춘셈
    """
    c104y = myredis.C104(code, 'c104y')
    c106y = myredis.C106(code, 'c106y')

    _, dict매출액증가율y = c104y.find_with_yoy('매출액증가율')

    c104q = myredis.C104(code, 'c104q')
    d2, 매출액증가율q = c104q.latest_value_pop2('매출액증가율')

    logger.debug(f'매출액증가율 : {매출액증가율q} {dict매출액증가율y}')

    ################################################################

    # c106 에서 타 기업과 영업이익률 비교
    dict영업이익률 = c106y.find('영업이익률')

    return {
        '매출액증가율': (매출액증가율q, dict매출액증가율y),
        '영업이익률': dict영업이익률,
        'date': [d2, ]}


"""
- 각분기의 합이 연이 아닌 타이틀(즉 sum_4q를 사용하면 안됨)
'*(지배)당기순이익'
'*(비지배)당기순이익'
'장기차입금'
'현금및예치금'
'매도가능금융자산'
'매도파생결합증권'
'만기보유금융자산'
'당기손익-공정가치측정금융부채'
'당기손익인식(지정)금융부채'
'단기매매금융자산'
'단기매매금융부채'
'예수부채'
'차입부채'
'기타부채'
'보험계약부채(책임준비금)'
'*CAPEX'
'ROE'
"""

"""
- sum_4q를 사용해도 되는 타이틀
'자산총계'
'당기순이익'
'유동자산'
'유동부채'
'비유동부채'

'영업활동으로인한현금흐름'
'재무활동으로인한현금흐름'
'ROIC'
"""
