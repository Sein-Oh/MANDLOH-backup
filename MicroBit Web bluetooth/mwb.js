var mwb = {}
mwb.uart ={
	service: {
		uuid: '6e400001-b5a3-f393-e0a9-e50e24dcca9e',
		callback: null,
	},
	dataTx: {uuid: '6e400002-b5a3-f393-e0a9-e50e24dcca9e'}, // microbit=>web
	dataRx: {uuid: '6e400003-b5a3-f393-e0a9-e50e24dcca9e'}, // web=>microbit
	device: null,
	callback: null,
}
// callback(x, y, z)
mwb.uart.start = function(callback) {
	if (!navigator.bluetooth) {
		alert("Error!")
		return
	}
	var $this = this;
	$this.callback = callback
	navigator.bluetooth.requestDevice({
		filters: [{
			namePrefix: 'BBC micro:bit'
		}],
		optionalServices: [$this.service.uuid] // to avoid Security Error
	})
	.then(device => {
		$this.device = device
		return device.gatt.connect()
	})
	.then(server => {
		return server.getPrimaryService($this.service.uuid)
	})
	.then(service => {
		$this.service.callback = service;
		service.getCharacteristic($this.dataTx.uuid)
		.then(characteristic => {
			characteristic.startNotifications()
			.then(() => {
				characteristic.addEventListener('characteristicvaluechanged', function (event) { // event handler
					var arr = [];
					for (var i = 0; i < this.value.byteLength; i++) {
						arr[i] = this.value.getUint8(i);
					}
					var str = String.fromCharCode.apply(null, arr);
					console.log("receive:", str);
					$this.callback(str)
				})
			})
		})
	})
	.catch(error => {
		console.log(error)
		alert(error)
	})
}

// https://makecode.microbit.org/_5Ya0KDTUvDUr
mwb.uart.send = function(str) {
	if (!this.service.callback)
		return
	this.service.callback.getCharacteristic(this.dataRx.uuid)
	.then(characteristic => {
		var arr = new Uint8Array(str.length);
		for (var i = 0; i < str.length; i++) {
			arr[i] = str[i].charCodeAt()
		}
		characteristic.writeValue(arr);
	})
}

mwb.uart.stop = function() {
	if (!this.device || !this.device.gatt.connected)
		return
	this.device.gatt.disconnect()
	this.callback('', '', '')
}
