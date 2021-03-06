import fcntl

from .base import DrmObject
from .drm_h import DRM_IOCTL_MODE_GETENCODER
from .drm_mode_h import DrmModeEncoderC, DRM_MODE_OBJECT_ENCODER, drm_encoder_type_name


#                ("encoder_id", c_uint32),
#                ("encoder_type", c_uint32),
#
#                ("crtc_id", c_uint32),
#
#                ("possible_crtcs", c_uint32),
#                ("possible_clones", c_uint32),


class DrmEncoder(DrmObject):
    def __init__(self, drm, id):
        self._drm = drm
        self.id = int(id)
        self.fetch()
        self._crtc = None # for inspect()

    def fetch(self):
        arg = DrmModeEncoderC()
        arg.encoder_id = self.id

        fcntl.ioctl(self._drm.fd, DRM_IOCTL_MODE_GETENCODER, arg)

        self._arg = arg
        self.type = arg.encoder_type

        self.crtc_id = arg.crtc_id
        self._possible_crtcs = arg.possible_crtcs
        self._possible_clones = arg.possible_clones

        self.type_name = drm_encoder_type_name(self.type)

        self.get_props(DRM_MODE_OBJECT_ENCODER)

    @property
    def crtc(self):
        if self.crtc_id:
            return self._drm.get_crtc(self.crtc_id)
        else:
            return None

    @property
    def possible_crtcs(self):
        return [crtc for i, crtc in enumerate(self._drm.crtcs) if (self._possible_crtcs >> i) & 1]

    @property
    def possible_clones(self):
        return [encoder for i, encoder in enumerate(self._drm.encoders) if (self._possible_clones >> i) & 1]
