// we use express and multer libraries to send images
const express = require('express');
const multer = require('multer');
const server = express();
const PORT = 3000;
const {spawn} = require('child_process');
const { response } = require('express');

var response_queue_poller;


var flag = false;


server.use(express.urlencoded());
server.use(express.json());


const controller = spawn('python', ['/home/ubuntu/ec2_controller/controller.py']);

controller.stdout.on('data', function(data) {
  console.log(data.toString());
});
controller.stderr.on('data', function(data) {
  console.log(data.toString());
});


// uploaded images are saved in the folder "/upload_images"
const upload = multer({dest: __dirname + '/upload_images'});

server.use(express.static('public'));

// "myfile" is the key of the http payload
server.post('/', upload.single('myfile'), function(request, respond) {
  if(request.file) console.log(request.file);
  console.log("Uploading " + request.file.originalname + " to S3");

  // Send the file to the request queue
  const request_queue_python = spawn('python', ['/home/ubuntu/s3_uploader/web_server_request_queue.py', request.file.originalname]);

  request_queue_python.stdout.on('data', function(data) {
    console.log(data.toString());
  });
  request_queue_python.stderr.on('data', function(data) {
    console.log(data.toString());
  });

  // save the image
  var fs = require('fs');
  fs.rename(__dirname + '/upload_images/' + request.file.filename, __dirname + '/upload_images/' + request.file.originalname, function(err) {
    if ( err ) console.log('ERROR: ' + err);
  });

  respond.end(request.file.originalname + ' uploaded!');
});



server.post('/response_queue', function(request, respond)
{
  console.log("Starting response queue poller", request.body.num);


    //code that causes an error
    const fs = require('fs');

    fs.unlink('/home/ubuntu/outputs.txt', (err => {
      if (err) console.log(err);
      else {
        console.log("\nDeleted file: /home/ubuntu/outputs.txt");

        // Get the files in current diectory
        // after deletion
      }
    }));
  response_queue_poller = spawn('python', ['/home/ubuntu/s3_uploader/results.py', request.body.num]);
// on poller printing (I think), take that data and save it in dictionary
// key: Image name, value: output pair, e.g. (test_0, bathtub)

  response_queue_poller.stdout.on('data', function(data)
  {
    console.log(data.toString());

  });
  response_queue_poller.stderr.on('data', function(data)
  {
    console.log(data.toString());

  });
  respond.end();

});

server.get("/kill", function(req, res){
  response_queue_poller.kill('SIGINT');
  res.send();

});

server.get("/", function(req, res){
  const path = "/home/ubuntu/outputs.txt";
  res.sendFile(path);


});

// You need to configure node.js to listen on 0.0.0.0 so it will be able to accept connections on all the IPs of your machine
const hostname = '0.0.0.0';
server.listen(PORT, hostname, () => {
    console.log(`Server running at http://${hostname}:${PORT}/`);
  });
