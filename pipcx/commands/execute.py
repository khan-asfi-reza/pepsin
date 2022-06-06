from pipcx.base import Base


class Command(Base):
    short_description = "Test Case"

    def execute(self, *args, **kwargs):
        print("Hello Worlds")
