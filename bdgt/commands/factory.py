from bdgt.commands import accounts


__all__ = ['CommandFactory']


class CommandFactory(object):
    @classmethod
    def create(cls, args):
        assert hasattr(args, 'command')

        if args.command == 'account':
            return AccountCommandFactory.create(args)
        else:
            assert False


class AccountCommandFactory(object):
    @classmethod
    def create(cls, args):
        assert hasattr(args, 'sub_command')

        if args.sub_command == 'add':
            return accounts.CmdAddAccount(args.name)
        elif args.sub_command == 'delete':
            return accounts.CmdDeleteAccount(args.name)
        elif args.sub_command == 'list':
            return accounts.CmdListAccounts()
        else:
            assert False
