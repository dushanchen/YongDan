from django.core.management.base import BaseCommand, CommandError

from operate.models import Authority, User, Role


class Command(BaseCommand):

    def handle(self, *args, **options):

        # 项目初始化操作

        print('创建权限...')
        
        # method 1 -> 'GET', 0 -> 'POST'

        # 用户管理
        user_authority = Authority.objects.get_or_create(name='user_platform', url='/operate/platform/', method=1, detail='平台用户管理')
        print(user_authority)
        Authority.objects.get_or_create(name='user_search', url='/operate/platform/?action=search', method=0, detail='查询用户', parent=user_authority[0])
        Authority.objects.get_or_create(name='user_create', url='/operate/user_save/?action=add', method=0, detail='新增用户', parent=user_authority[0])
        Authority.objects.get_or_create(name='user_edit', url='/operate/platform/?action=edit', method=0, detail='修改用户', parent=user_authority[0])
        Authority.objects.get_or_create(name='user_edit_role', url='/operate/platform/?action=edit_role', method=0, detail='修改用户角色', parent=user_authority[0])
        Authority.objects.get_or_create(name='user_status', url='/operate/dostatus/', method=0, detail='停用/启用', parent=user_authority[0])
        Authority.objects.get_or_create(name='user_edit_password', url='/operate/dostatus/?action=edit_passwod', method=0, detail='修改用户密码', parent=user_authority[0])
        

        # 角色管理
        role_authority = Authority.objects.get_or_create(name='role_list', url='/operate/role/', method=1, detail='角色管理')
        print(role_authority)
        Authority.objects.get_or_create(name='role_create', url='/operate/role_save/?action=add', method=0, detail='新增角色', parent=role_authority[0])
        Authority.objects.get_or_create(name='role_edit', url='/operate/role_save/?action=edit', method=0, detail='修改角色', parent=role_authority[0])
        

        #修改密码
        password_authority = Authority.objects.get_or_create(name='alter_password', url='/operate/alterpassword/', method=1, detail='修改密码')


        self.stdout.write(self.style.SUCCESS('创建权限完成'))


        if not Role.objects.filter(name='admin').exists():
            Role.objects.create(name='admin',detail='系统管理员, 最高权限')
            self.stdout.write(self.style.SUCCESS('创建管理员角色'))

        if not User.objects.exists():
            role = Role.objects.filter(name='管理员').first()

            admin = Administrator.objects.create(name='admin', password='111111')
            admin.role.add(role)
            self.stdout.write(self.style.SUCCESS('创建管理员用户!'))


