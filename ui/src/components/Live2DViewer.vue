<template>
  <video ref="screenStreamVideo" class="absolute top-0 left-0 w-full -z-100" autoplay></video>
  <canvas ref="live2dCanvas" class="z-100"></canvas>
</template>

<script setup>
import { onMounted, ref, toRef, watch } from 'vue'
import * as PIXI from 'pixi.js'
import { Live2DModel } from 'pixi-live2d-display-lipsyncpatch/cubism4';

const props = defineProps({
  isStreamOn: Boolean,
})

const isStreamOn = toRef(props, 'isStreamOn')
window.PIXI = PIXI
let screenStream = null
const screenStreamVideo = ref(null)
const live2dCanvas = ref(null)
const centerX = window.innerWidth / 2
const centerY = window.innerHeight / 2

const toggleScreenStream = async () => {
  if (screenStream) {
    screenStream.getTracks().forEach(track => track.stop())
    screenStream = null
    screenStreamVideo.value.srcObject = null
  } else {
    try {
      screenStream = await navigator.mediaDevices.getDisplayMedia({
        video: { mediaSource: "screen" }
      });

      screenStreamVideo.value.srcObject = screenStream;
      screenStreamVideo.value.onloadedmetadata = () => {
        function drawFrame() {
          if (screenStream.active) {
            requestAnimationFrame(drawFrame)
          }
        }

        drawFrame()
      };
    } catch (err) {
      console.error("Error capturing screen:", err)
    }
  }
}

const draggable = (model) => {
  model.x = centerX
  model.y = centerY
  model.anchor.set(0.5, 0.5)

  let dragging = false;
  model.on("pointerdown", (e) => (dragging = true))
  model.on("pointermove", (e) => {
    if (dragging) {
      model.x = e.data.global.x
      model.y = e.data.global.y
    }
  });
  model.on("pointerupoutside", () => (dragging = false))
  model.on("pointerup", () => (dragging = false))
}

const zoom = (model) => {
  let scaleFactor = 0.1;
  model.scale.set(scaleFactor, scaleFactor)
  model.on('wheel', (e) => {
    const minScale = 0.05;
    const maxScale = 0.5;
    const zoomSpeed = 0.0001;
    const delta = -e.deltaY * zoomSpeed;

    scaleFactor += delta;
    scaleFactor = Math.min(maxScale, Math.max(minScale, scaleFactor));

    model.scale.set(scaleFactor, scaleFactor);
  })
}

const lerp = (start, end, t) => {
  return start + (end - start) * t
}

const lookCursor = (model, app) => {
  let targetParams = { angleX: 0, angleY: 0, eyeX: 0, eyeY: 0 }
  let currentParams = { angleX: 0, angleY: 0, eyeX: 0, eyeY: 0 }
  let lookCursorTimeout

  app.ticker.add(() => {
    const smoothing = 0.3

    currentParams.angleX = lerp(currentParams.angleX, targetParams.angleX, smoothing)
    currentParams.angleY = lerp(currentParams.angleY, targetParams.angleY, smoothing)
    currentParams.eyeX = lerp(currentParams.eyeX, targetParams.eyeX, smoothing)
    currentParams.eyeY = lerp(currentParams.eyeY, targetParams.eyeY, smoothing)

    model.internalModel.coreModel.setParameterValueById('ParamAngleX', currentParams.angleX)
    model.internalModel.coreModel.setParameterValueById('ParamAngleY', currentParams.angleY)
    model.internalModel.coreModel.setParameterValueById('ParamEyeBallX', currentParams.eyeX)
    model.internalModel.coreModel.setParameterValueById('ParamEyeBallY', currentParams.eyeY)
  })

  window.addEventListener('mousemove', (e) => {
    const maxAngle = 30
    const dx = (e.clientX - centerX) / centerX
    const dy = (e.clientY - centerY) / centerY

    const clamp = (val, min, max) => Math.max(min, Math.min(val, max))
    targetParams.angleX = clamp(dx, -1, 1) * maxAngle
    targetParams.angleY = clamp(-dy, -1, 1) * maxAngle
    targetParams.eyeX = clamp(dx, -1, 1)
    targetParams.eyeY = clamp(-dy, -1, 1)

    model.internalModel.coreModel.setParameterValueById('ParamAngleX', currentParams.angleX)
    model.internalModel.coreModel.setParameterValueById('ParamAngleY', currentParams.angleY)
    model.internalModel.coreModel.setParameterValueById('ParamEyeBallX', currentParams.eyeX)
    model.internalModel.coreModel.setParameterValueById('ParamEyeBallY', currentParams.eyeY)

    if (lookCursorTimeout) clearTimeout(lookCursorTimeout)
    lookCursorTimeout = window.setTimeout(() => {
      targetParams = { angleX: 0, angleY: 0, eyeX: 0, eyeY: 0 }
    }, 1500)
  })
}

const hit = (model) => {
  model.on('pointerdown', (e) => {
    model.internalModel.coreModel.setParameterValueById('ParamEyeLOpen', 0)

    idleTimeout = window.setTimeout(() => {
      model.internalModel.coreModel.setParameterValueById('ParamEyeLOpen', 1)
    }, 2000)
  })
}

onMounted(async () => {
  const app = new PIXI.Application({
    view: live2dCanvas.value,
    autoStart: true,
    width: window.innerWidth,
    height: window.innerHeight,
    backgroundAlpha: 0,
  })
  const model = await Live2DModel.from('/models/poblanc/Poblanc.model3.json')
  app.stage.addChild(model)
  model.interactive = true
  model.buttonMode = true

  lookCursor(model, app)
  draggable(model)
  zoom(model)
  hit(model)
})

watch(isStreamOn, (newVal, oldVal) => {
  toggleScreenStream()
})
</script>
