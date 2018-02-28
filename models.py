# -*- coding: utf-8 -*-
from collections import namedtuple
from flask_login import UserMixin

Size = namedtuple('Size', ['width', 'height', 'depth'])


class BoundingBox:
    def __init__(self, relative_x, relative_y, relative_width, relative_height,
                 img_width, img_height):
        self._x_min = relative_x * img_width
        self._y_min = relative_y * img_height
        self._x_max = self._x_min + relative_width * img_width
        self._y_max = self._y_min + relative_height * img_height

    @property
    def x_min(self):
        return self._x_min

    @property
    def y_min(self):
        return self._y_min

    @property
    def x_max(self):
        return self._x_max

    @property
    def y_max(self):
        return self._y_max

    def __str__(self):
        return self.__repr__() + '\nx_min: %s\nx_max: %s\ny_min: %s\ny_max: %s' % (
            self.x_min, self.x_max, self.y_min, self.y_max
        )


class Object:
    def __init__(self, name, bounding_box):
        self._name = name
        self._pose = 'Unspecified'
        self._truncated = 0
        self._difficult = 0
        self._bounding_box = bounding_box

    @property
    def name(self):
        return self._name

    @property
    def pose(self):
        return self._pose

    @property
    def truncated(self):
        return self._truncated

    @property
    def difficult(self):
        return self._difficult

    @property
    def bounding_box(self):
        return self._bounding_box

    def __str__(self):
        return self.__repr__() + '\nname: %s\npose: %s\ntruncated: %s\ndifficult: %s\nbounding_box: %s' % (
            self.name, self.pose, self.truncated, self.difficult, self.bounding_box
        )


class Annotations:
    def __init__(self, annotations):
        if len(annotations) == 0:
            raise ValueError('Annotations is empty')
        self.annotations = annotations

    def __iter__(self):
        for annotation in self.annotations:
            label = annotation['text']
            geometry = annotation['shapes'][0]['geometry']
            bounding_box = BoundingBox(relative_x=geometry['x'],
                                       relative_y=geometry['y'],
                                       relative_width=geometry['width'],
                                       relative_height=geometry['height'],
                                       img_width=500,
                                       img_height=343)
            yield label, bounding_box

    def __str__(self):
        return self.__repr__() + '\n' + str(self.annotations)


class User(UserMixin):
    __shared_state = {}

    def __init__(self):
        self.__dict__ = self.__shared_state
        self._id = 0
        self._username = "bingbinadmin"
        self._password = ":k}5#%e%kzJ}rNAY_qF4}28d{UDY>hx2"

    @property
    def id(self):
        return self._id

    @property
    def password(self):
        return self._password

    @property
    def username(self):
        return self._username

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

    def __str__(self):
        return str(self.username)


class DB:
    @classmethod
    def find_user(cls, id=None, username=None):
        if username == "bingbinadmin" or id == 0:
            return User()
        return None
