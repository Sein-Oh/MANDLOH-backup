//224x224로 세팅된 이미지를 사용한 경우.
//v1 : Pre-training 없는 경우.
const tf = require("@tensorflow/tfjs");
const path = require("path");
const fs = require("fs");
const { createCanvas, loadImage } = require("canvas");
const imgSize = 224;
const canvas = createCanvas(imgSize, imgSize);
const ctx = canvas.getContext("2d");

async function getImgPath(dir, ext) {
  const fileName = fs.readdirSync(dir).filter((file) => file.endsWith(ext)); //특정 확장자로 필터링
  return fileName.map((file) => path.join(dir, file));
}

async function buildObjectDetectionModel() {
  const truncatedBase = await loadTruncatedBase();
  const newHead = buildNewHead(truncatedBase.outputs[0].shape.slice(1));
  const newOutput = newHead.apply(truncatedBase.outputs[0]);
  const model = tf.model({ inputs: truncatedBase.inputs, outputs: newOutput });
  return model;
}

async function loadTruncatedBase() {
  const topLayerGroupNames = ["conv_pw_9", "conv_pw_10", "conv_pw_11"];
  const topLayerName = `${topLayerGroupNames[topLayerGroupNames.length - 1]}_relu`;
  const mobilenet = await tf.loadLayersModel("https://storage.googleapis.com/tfjs-models/tfjs/mobilenet_v1_0.25_224/model.json");
  const layer = mobilenet.getLayer(topLayerName);
  const truncatedBase = tf.model({
    inputs: mobilenet.inputs,
    outputs: layer.output,
  });
  return truncatedBase;
}

function buildNewHead(inputShape) {
  const newHead = tf.sequential();
  newHead.add(tf.layers.flatten({ inputShape }));
  newHead.add(tf.layers.dense({ units: 200, activation: "relu" }));
  newHead.add(tf.layers.dense({ units: 4 }));
  return newHead;
}

async function* dsGen() {
  for (let i = 0; i < imgPathAry.length; i++) {
    const bbox_str = imgPathAry[i].split("_")[2].split(".")[0].split(",");
    const bbox = bbox_str.map((e) => parseInt(e));
    const y = tf.tensor1d(bbox);
    const img = await loadImage(imgPathAry[i]);
    ctx.drawImage(img, 0, 0, imgSize, imgSize);
    const x = tf.browser.fromPixels(canvas).div(255.0);
    yield { xs: x, ys: y };
  }
}

let imgPathAry;
async function main() {
  const imgExt = "jpg";
  const datasetPath = "new_image";
  imgPathAry = await getImgPath(datasetPath, imgExt);
  console.log(`Found ${imgPathAry.length} images.`);
  const ds = tf.data.generator(dsGen).batch(12);
  const model = await buildObjectDetectionModel();
  console.log("Start training...");
  model.compile({ loss: 'meanSquaredError', optimizer: tf.train.adam() });
  await model.fitDataset(ds, {
    epochs: 30,
  });
  await model.save("file://model_cpu");
  console.log("training complete");
}

main();
