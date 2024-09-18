class Program:
    def __call__(self, **kwargs):
        return self.forward(**kwargs)
    def forward(self, **kwargs):
        pass