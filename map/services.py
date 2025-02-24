from django.core.files.uploadedfile import TemporaryUploadedFile

from PIL import Image
from PIL import ExifTags
from PIL.ExifTags import GPSTAGS, TAGS


class PhotoMetaDataService:
    def get_metadata(self, image_file: TemporaryUploadedFile) -> dict:
        meta, data = {}, {}
        image = Image.open(image_file.temporary_file_path())
        exifdata = image.getexif()

        for tagid in exifdata:
            tagname = TAGS.get(tagid, tagid)
            value = exifdata.get(tagid)
            meta |= {tagname: value}

        ifd = exifdata.get_ifd(0x8825)
        for key, val in ifd.items():
            data[ExifTags.GPSTAGS[key]] = val

        meta['GPSInfo'] = data

        return meta

    def _convert_to_degrees(self, value) -> float:
        """
        Helper function to convert the GPS coordinates stored
        in the EXIF to degrees in float format.
        """
        # TODO: value parameter should be tuple in format "(59.0, 52.0, 25.43)"

        d0 = value[0][0]
        d1 = value[0][1]
        d = float(d0) / float(d1)

        m0 = value[1][0]
        m1 = value[1][1]
        m = float(m0) / float(m1)

        s0 = value[2][0]
        s1 = value[2][1]
        s = float(s0) / float(s1)

        return d + (m / 60.0) + (s / 3600.0)

    def get_lat_lon(self, exif_data: dict) -> tuple[float, float]:
        """
        Returns the latitude and longitude, if available,
        from the provided exif_data (obtained through get_exif_data).
        """
        lat = None
        lon = None

        if 'GPSInfo' in exif_data:
            gps_info = exif_data['GPSInfo']

            gps_latitude = gps_info.get('GPSLatitude')
            gps_latitude_ref = gps_info.get('GPSLatitudeRef')
            gps_longitude = gps_info.get('GPSLongitude')
            gps_longitude_ref = gps_info.get('GPSLongitudeRef')

            if gps_latitude and gps_latitude_ref and gps_longitude and gps_longitude_ref:
                lat = self._convert_to_degrees(gps_latitude)
                if gps_latitude_ref != 'N':
                    lat = 0 - lat

                lon = self._convert_to_degrees(gps_longitude)
                if gps_longitude_ref != 'E':
                    lon = 0 - lon

        return lat, lon
