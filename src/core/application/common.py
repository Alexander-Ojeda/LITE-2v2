#src\core\application\common.py
class Command:
    pass

class UseCase:
    def execute(self, command: Command):
        raise NotImplementedError