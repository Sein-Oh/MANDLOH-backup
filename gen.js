const tf = require('@tensorflow/tfjs-node');
const path = require('path');
const fs = require('fs');
const { createCanvas, loadImage } = require('canvas');
const imgSize = 224;
const imgExt = "png";
const canvas = createCanvas(imgSize, imgSize);
const ctx = canvas.getContext('2d');

async function buildObjectDetectionModel() {
    const { truncatedBase, fineTuningLayers } = await loadTruncatedBase();
    const newHead = buildNewHead(truncatedBase.outputs[0].shape.slice(1));
    const newOutput = newHead.apply(truncatedBase.outputs[0]);
    const model = tf.model({ inputs: truncatedBase.inputs, outputs: newOutput });

    return [model, fineTuningLayers];
}

async function loadTruncatedBase() {
    const topLayerGroupNames = ['conv_pw_9', 'conv_pw_10', 'conv_pw_11'];
    const topLayerName = `${topLayerGroupNames[topLayerGroupNames.length - 1]}_relu`;
    const mobilenet = await tf.loadLayersModel('https://storage.googleapis.com/tfjs-models/tfjs/mobilenet_v1_0.25_224/model.json');
    const fineTuningLayers = [];
    const layer = mobilenet.getLayer(topLayerName);
    const truncatedBase = tf.model({ inputs: mobilenet.inputs, outputs: layer.output });
    for (const layer of truncatedBase.layers) {
        for (const groupName of topLayerGroupNames) {
            if (layer.name.indexOf(groupName) === 0) {
                fineTuningLayers.push(layer);
                break;
            }
        }
    }
    return { truncatedBase, fineTuningLayers };
}

function buildNewHead(inputShape) {
    const newHead = tf.sequential();
    newHead.add(tf.layers.flatten({ inputShape }));
    newHead.add(tf.layers.dense({ units: 200, activation: 'relu' }));
    //newHead.add(tf.layers.dense({ units: 5 }));
    newHead.add(tf.layers.dense({ units: 4 }));
    return newHead;
}

function getImagePath(dir, ext){
    const fileName = fs.readdirSync(dir).filter((file) => file.endsWith(ext));  //특정 확장자로 필터링
    return fileName.map(file => path.join(dir, file));
}

async function imgToTensor(imgPath){
    const img = await loadImage(imgPath);
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    if (img.width > img.height) {
        let sc = imgSize/img.width;
        ctx.drawImage(img, 0, 0, img.width, img.height, 0, (img.width-img.height)/2*sc, img.width*sc, img.height*sc);
    } else {
        let sc = imgSize/img.height;
        ctx.drawImage(img, 0, 0, img.width, img.height, (img.height-img.width)/2*sc, 0, img.width*sc, img.height*sc);
    }
    return await tf.browser.fromPixels(canvas).div(255.0).expandDims();
}

async function makeDataSet(xs, ys, path){
    const txtPath = path.replace(imgExt, "txt");
    const f = fs.readFileSync(txtPath, 'utf8');
    let bbox = [];
    let index = f.indexOf('Ymax');
    const index_start1 = f.indexOf('(', index);
    const index_end1 = f.indexOf(')', index_start1);
    const box1 = f.substring(index_start1 + 1, index_end1).replace(' ', '').split(',').map(t=>parseInt(t));
    const index_start2 = f.indexOf('(', index_end1);
    const index_end2 = f.indexOf(')', index_start2);
    const box2 = f.substring(index_start2 + 1, index_end2).replace(' ', '').split(',').map(t=>parseInt(t));
    //box1.unshift(1); //for the probability.
    bbox.push(box1.concat(box2));
    const x = await imgToTensor(path);
    const y = tf.tensor(bbox);
    (xs == undefined) ? xs = x : xs = xs.concat(x);
    (ys == undefined) ? ys = y : ys = ys.concat(y);
    return [xs, ys];
}

async function makeLabelSet(path){
    const txtPath = path.replace(imgExt, "txt");
    const f = fs.readFileSync(txtPath, 'utf8');
    let bbox = [];
    let index = f.indexOf('Ymax');
    const index_start1 = f.indexOf('(', index);
    const index_end1 = f.indexOf(')', index_start1);
    const box1 = f.substring(index_start1 + 1, index_end1).replace(' ', '').split(',').map(t=>parseInt(t));
    const index_start2 = f.indexOf('(', index_end1);
    const index_end2 = f.indexOf(')', index_start2);
    const box2 = f.substring(index_start2 + 1, index_end2).replace(' ', '').split(',').map(t=>parseInt(t));
    bbox.push(box1.concat(box2));
    return bbox;
}

async function makeImgSet(path){
    const img = await loadImage(path);
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    if (img.width > img.height) {
        let sc = imgSize/img.width;
        ctx.drawImage(img, 0, 0, img.width, img.height, 0, (img.width-img.height)/2*sc, img.width*sc, img.height*sc);
    } else {
        let sc = imgSize/img.height;
        ctx.drawImage(img, 0, 0, img.width, img.height, (img.height-img.width)/2*sc, 0, img.width*sc, img.height*sc);
    }
    return canvas;
}

function* dsGen() {
    for (let i=0; i< imgPathAry.length; i++) {
        const x = tf.browser.fromPixels(imgDataAry[i]).div(255.0);
        const y = tf.tensor(labelAry[i]);
        yield {xs : x, ys : y}
    }
}

let imgPathAry = [];
let imgDataAry = [];
let labelAry = [];
async function main(){
    const datasetFoler = "people";
    imgPathAry = getImagePath(datasetFoler, imgExt);
    for (p of imgPathAry) {
        imgDataAry.push(await makeImgSet(p));
        labelAry.push(await makeLabelSet(p));
    }
    console.log(`imgDataAry length : ${imgDataAry.length}`);
    console.log(`labelAry length : ${labelAry.length}`);
    let xs, ys;
    for (imgData of imgDataAry) {
        const x = tf.browser.fromPixels(imgData).div(255.0).expandDims();
        (xs == undefined) ? xs = x : xs = xs.concat(x);
    }
    console.log(xs.shape);
    for (label of labelAry) {
        const y = tf.tensor(label);
        (ys == undefined) ? ys = y : ys = ys.concat(y);
    }
    console.log(ys.shape);
    //const ds = tf.data.generator(dsGen).batch(32).shuffle(imgPathAry.length);
    const [model, fineTuningLayers] = await buildObjectDetectionModel();
    await model.compile({loss:'meanSquaredError', optimizer: tf.train.rmsprop(5e-3)});
    console.log('Start 1st training...');
    await model.fit(xs, ys, {
        epochs: 20
    });

    for  (const layer of fineTuningLayers) {
        layer.trainable = true;
    }
    model.compile({loss: 'meanSquaredError', optimizer: tf.train.rmsprop(2e-3)});

    await model.fit(xs, ys, {
        epochs : 50
    });


    /*
    await model.fitDataset(ds, {
        epochs: 20
    });
    
    for  (const layer of fineTuningLayers) {
        layer.trainable = true;
    }
    console.log('Start 2nd training...');
    await model.compile({ loss: 'meanSquaredError', optimizer: tf.train.rmsprop(2e-3) });
    await model.fitDataset(ds, {
        epochs: 50
    });
    await model.save("file://model_gen");
    console.log('training complete');
    */
}

main() 
