from viggocore.common import manager, exception
from viggocore.common.subsystem import operation
from viggocore.common.subsystem.pagination import Pagination
from viggocore.subsystem.capability_module.resource \
    import CapabilityModule
from viggocore.subsystem.policy_module.resource \
    import PolicyModule
from viggocore.subsystem.module.resource \
    import Module
from sqlalchemy import or_


class GetAvailableModules(operation.List):

    def pre(self, **kwargs):
        self.role_id = kwargs.get('role_id', None)
        if self.role_id is None:
            raise exception.BadRequest('Role_id is required')
        return super().pre(**kwargs)

    def do(self, session, **kwargs):
        query = session.query(CapabilityModule, Module). \
            join(Module,
                 CapabilityModule.module_id == Module.id). \
            join(PolicyModule,
                 PolicyModule.capability_module_id ==  # noqa
                 CapabilityModule.id, isouter=True). \
            filter(
                or_(PolicyModule.role_id != self.role_id,
                    PolicyModule.role_id == None))  # noqa
        query = self.manager.apply_filters(query, CapabilityModule, **kwargs)
        query = query.distinct()

        dict_compare = {'module.': Module,
                        'policy_module.': PolicyModule}
        query = self.manager.apply_filters_includes(
            query, dict_compare, **kwargs)
        query = query.distinct()

        total_rows = None
        if self.manager.with_pagination(**kwargs):
            total_rows = query.count()

        pagination = Pagination.get_pagination(Module, **kwargs)
        if pagination.order_by is not None:
            pagination.adjust_order_by(Module)
        query = self.driver.apply_pagination(query, pagination)
        result = query.all()
        response = [r[0] for r in result]

        return (response, total_rows)


class GetSelectedModules(operation.List):

    def pre(self, **kwargs):
        self.role_id = kwargs.get('role_id', None)
        if self.role_id is None:
            raise exception.BadRequest('Role_id is required')
        return super().pre(**kwargs)

    def do(self, session, **kwargs):
        query = session.query(CapabilityModule, PolicyModule.id, Module). \
            join(Module,
                 CapabilityModule.module_id == Module.id). \
            join(PolicyModule,
                 PolicyModule.capability_module_id ==  # noqa
                 CapabilityModule.id, isouter=True). \
            filter(
                PolicyModule.role_id == self.role_id)
        query = self.manager.apply_filters(query, Module, **kwargs)
        query = query.distinct()

        dict_compare = {'module.': Module,
                        'policy_module.': PolicyModule}
        query = self.manager.apply_filters_includes(
            query, dict_compare, **kwargs)
        query = query.distinct()

        total_rows = None
        if self.manager.with_pagination(**kwargs):
            total_rows = query.count()

        pagination = Pagination.get_pagination(Module, **kwargs)
        if pagination.order_by is not None:
            pagination.adjust_order_by(Module)
        query = self.driver.apply_pagination(query, pagination)
        result = query.all()
        response = [(r[0], r[1]) for r in result]

        return (response, total_rows)


class Delete(operation.Delete):

    def pre(self, session, id, **kwargs):
        super().pre(session, id=id)
        policies = self.manager.api.policy_modules().list(
            policy_module_id=id)
        if policies:
            message = 'You can\'t remove this capability because' + \
                ' there are policies associated'
            raise exception.BadRequest(message)
        return True


class Manager(manager.CommonManager):

    def __init__(self, driver):
        super(Manager, self).__init__(driver)
        self.get_available_modules = GetAvailableModules(self)
        self.get_selected_modules = GetSelectedModules(self)
        self.delete = Delete(self)
