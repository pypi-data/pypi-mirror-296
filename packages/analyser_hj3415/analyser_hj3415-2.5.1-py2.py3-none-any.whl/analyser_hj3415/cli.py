import argparse
from utils_hj3415 import noti


def analyser():
    from analyser_hj3415.myredis import red_ranking, mil_n_score
    commands = {
        'ranking': red_ranking,
        'mil': mil_n_score,
    }
    parser = argparse.ArgumentParser()
    parser.add_argument('command', help=f"Commands - {commands.keys()}")
    parser.add_argument('--noti', action='store_true', help='작업완료후 메시지 전송여부')

    args = parser.parse_args()

    if args.command in commands.keys():
        if args.command == 'ranking':
            print(commands['ranking']())
            if args.noti:
                noti.telegram_to('manager', "오늘의 red ranking을 레디스캐시에 저장했습니다.(유효 12시간)")
        elif args.command == 'mil':
            print("**** mil_n_score ****")
            for code, _ in red_ranking().items():
                print("<<<<< ", code, ">>>>>")
                print(commands['mil'](code))
            if args.noti:
                noti.telegram_to('manager', "오늘의 mil and score를 레디스캐시에 저장했습니다.(유효 12시간)")
    else:
        print(f"The command should be in {list(commands.keys())}")


