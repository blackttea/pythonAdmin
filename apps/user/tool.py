# dict 转 实体对象
class objDictTool:
    @staticmethod
    def to_obj(obj: object, **data):
        obj.__dict__.update(data)
