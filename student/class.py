class Person:
    r_rus='абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
    R_RUS=r_rus.upper()
    def __init__(self,fio,old,ps,weight):
        self.verify_fio(fio)
        self.verify_old(old)
        self.verify_weight(weight)
        self.verify_ps(ps)

        self.__fio=fio.split()
        self.__old=old
        self.__ps = ps
        self.__weight=weight
    @classmethod
    def verify_fio(cls,fio):
        if type(fio)!=str:
            raise TypeError("ФИО должно быть строкой")
        f=fio.split()
        if len(f)!=3:
            raise TypeError("Должно быть ровно три слова")
        letters=cls.r_rus+cls.R_RUS
        for s in f:
            if len(s)<1:
                raise TypeError("Каждый элемент ФИО должен состоять из более чем одного символа")
            if len(s.strip(letters))!=0:
                raise TypeError("Использован не верный символ")
    @classmethod
    def verify_old(cls,old):
        if type(old)!=int:
            raise TypeError("Возраст должен быть в виде числа")
        if old<14 or old>120:
            raise TypeError("Неверный возраст [14-120]")

    @classmethod
    def verify_weight(cls, weight):
        if type(weight) != float:
            raise TypeError("Вec должен быть в виде числа")
        if weight < 20:
            raise TypeError("Неверный вес.Должен быть больше 20")
    @classmethod
    def verify_ps(cls,ps):
        if type(ps)!=str:
            raise TypeError("Паспорт должен быть строкой")
        s=ps.split()
        if len(s)!=2:
            raise TypeError("Введен неверный формат")
        if len(s[0])!=4:
                raise TypeError("Введен неверный формат")
        if len(s[1])!=6:
            raise TypeError("Введен неверный формат")
        for p in s:
            if p.isdigit()==False:
                raise TypeError("Используйте только цифры")

    @property
    def fio(self):
        return self.__fio
    @fio.setter
    def fio(self,fio):
        self.verify_fio(fio)
        self.__fio=fio
    







prs1=Person('Зубенко Михаил Петрович',28,'5676 656989',20.1)
prs1.fio='Дмитрий Желзо Любик'
print(prs1.__dict__)

