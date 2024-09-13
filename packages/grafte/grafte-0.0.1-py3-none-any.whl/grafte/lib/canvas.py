from collections import namedtuple


class CanvasConfig(dict):
    def __init__(self, *args, **kwargs):
        # If args are provided, assume it might be a namedtuple or dict
        if args:
            config_source = args[0]
            if isinstance(config_source, dict):
                # Initialize from dict
                super().__init__(config_source)
                self._init_from_dict(config_source)
            elif isinstance(config_source, tuple) and hasattr(config_source, "_fields"):
                # Initialize from namedtuple
                config_dict = config_source._asdict()
                super().__init__(config_dict)
                self._init_from_dict(config_dict)
        else:
            # Initialize from kwargs if no args are provided
            super().__init__(**kwargs)
            self._init_from_dict(kwargs)

        # Handle additional kwargs or defaults if not provided
        self.background_color = kwargs.get(
            "background-color", self.get("background-color", "white")
        )
        self.dpi = kwargs.get("dpi", self.get("dpi", 72))
        self.width = kwargs.get("width", self.get("width", 900))
        self.height = kwargs.get("height", self.get("height", 600))
        self.width_inches = self.width / self.dpi
        self.height_inches = self.height / self.dpi

    def _init_from_dict(self, config_dict):
        """Helper method to initialize attributes from a dict or namedtuple."""
        for key, value in config_dict.items():
            self[key] = value
            setattr(self, key.replace("-", "_"), value)  # Update attributes too

    def update_from_dict(self, config_dict):
        """Update CanvasConfig with values from another dict."""
        self._init_from_dict(config_dict)
        # Recalculate width and height in inches if changed
        self.width_inches = self.width / self.dpi
        self.height_inches = self.height / self.dpi

    def config_matplotlib_figure(self, plt):
        """Return a fig"""
        _c = self.to_matplotlib_config()
        fig = plt.figure(
            figsize=_c["figsize"], dpi=_c["dpi"], facecolor=_c["facecolor"]
        )
        return fig

    def to_matplotlib_config(self) -> dict:
        d = {}
        d["figsize"] = (self.width_inches, self.height_inches)
        d["dpi"] = self.dpi
        d["facecolor"] = self.background_color
        return d
