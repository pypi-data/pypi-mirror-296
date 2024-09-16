import os
import argparse
from utils_hj3415.utils import SettingsManager

# 파일 경로 상수
SETTINGS_FILE = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'settings.json')

# 기본 주소
DEFAULT_MONGO_ADDR = 'mongodb://hj3415:piyrw421@localhost:27017'
DEFAULT_REDIS_ADDR = 'localhost'

class DbSettingsManager(SettingsManager):
    DB_TYPE = ['mongo', 'redis']

    def set_address(self, db_type: str, address: str):
        assert db_type in self.DB_TYPE, f"db_type 인자는 {self.DB_TYPE} 중에 있어야 합니다."
        self.settings_dict[f"{db_type}_addr"] = address
        self.save_settings()
        print(f"{db_type} 주소가 저장되었습니다: {address}")

    def get_address(self, db_type: str) -> str:
        assert db_type in self.DB_TYPE, f"db_type 인자는 {self.DB_TYPE} 중에 있어야 합니다."
        default_addr = DEFAULT_MONGO_ADDR if db_type == 'mongo' else DEFAULT_REDIS_ADDR
        return self.settings_dict.get(f"{db_type}_addr", default_addr)

    def reset_address(self, db_type: str):
        assert db_type in self.DB_TYPE, f"db_type 인자는 {self.DB_TYPE} 중에 있어야 합니다."
        default_addr = DEFAULT_MONGO_ADDR if db_type == 'mongo' else DEFAULT_REDIS_ADDR
        self.set_address(db_type, default_addr)
        print(f"{db_type} 주소가 기본값 ({default_addr}) 으로 초기화 되었습니다.")


def db_manager():
    settings_manager = DbSettingsManager(SETTINGS_FILE)

    parser = argparse.ArgumentParser(description="데이터베이스 주소 관리 프로그램")
    subparsers = parser.add_subparsers(dest='db_type', help='데이터베이스 종류를 지정하세요(mongo, redis)')

    for db in ['mongo', 'redis']:
        db_parser = subparsers.add_parser(db, help=f"{db} 주소를 관리합니다.")
        db_subparsers = db_parser.add_subparsers(dest='command', help='명령을 선택하세요.')

        # save 명령어
        save_parser = db_subparsers.add_parser('save', help=f"{db} 주소를 저장합니다.")
        save_parser.add_argument('address', type=str, help=f"저장할 {db} 주소를 입력하세요.")

        # print 명령어
        db_subparsers.add_parser('print', help=f"{db} 주소를 출력합니다.")

        # reset 명령어
        db_subparsers.add_parser('reset', help=f"{db} 주소를 기본값으로 초기화합니다.")

    args = parser.parse_args()

    if args.db_type:
        if args.command == 'save':
            settings_manager.set_address(args.db_type, args.address)
        elif args.command == 'print':
            address = settings_manager.get_address(args.db_type)
            print(f"{args.db_type} 주소: {address}")
        elif args.command == 'reset':
            settings_manager.reset_address(args.db_type)
        else:
            parser.print_help()
    else:
        parser.print_help()

def set_address_for_developing():
    # 테스트 서버 주소
    TEST_MONGO_ADDR = "mongodb+srv://Cluster13994:Rnt3Q1hrZnFT@cluster13994.vhtfyhr.mongodb.net"
    TEST_REDIS_ADDR = "localhost"

    setting_manager = DbSettingsManager(SETTINGS_FILE)
    setting_manager.set_address('mongo', 'mongodb://hj3415:piyrw421@192.168.100.175:27017')
    setting_manager.set_address('redis', '192.168.100.176')
    print(setting_manager.load_settings())
