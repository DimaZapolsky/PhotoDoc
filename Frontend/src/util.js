import imagesLoaded from 'imagesloaded'
import EXIF from 'exif-js'

const rotateAngles = [
  {},
  { y: 0, z: 0 },
  { y: 180, z: 0 },
  { y: 0, z: 180 },
  { y: 180, z: 180 },
  { y: 180, z: -90 },
  { y: 0, z: -90 },
  { y: 180, z: 90 },
  { y: 0, z: 90 }
]

export function getOrientation(el) {
  return new Promise(function (resolve, reject) {
    imagesLoaded(el, function () {
      EXIF.getData(el, function () {
        const orientation = EXIF.getTag(this, 'Orientation')
        resolve(orientation)
      })
    })
  })
}

export function getRotationAngle(newOrientation, oldOrientation) {
  const y = rotateAngles[newOrientation].y - rotateAngles[oldOrientation].y
  let z = rotateAngles[newOrientation].z - rotateAngles[oldOrientation].z
  if (y) {
    z = z * -1
  }
  return {
    y,
    z
  }
}