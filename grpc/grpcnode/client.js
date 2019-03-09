var grpc = require('grpc');
var protoLoader = require('@grpc/proto-loader');
var fs = require('fs');

var PROTO_PATH = __dirname + '/proto/helloworld.proto';

var packageDefinition = protoLoader.loadSync(
    PROTO_PATH,
    {keepCase: true,
     longs: String,
     enums: String,
     defaults: true,
     oneofs: true
    });

var hello_proto = grpc.loadPackageDefinition(packageDefinition).helloworld;

function main() {
    let credentials = grpc.credentials.createSsl(
        fs.readFileSync('./keys/ca.crt'),
     fs.readFileSync('./keys/client.key'), 
     fs.readFileSync('./keys/client.crt'));

    const cacert = fs.readFileSync('keys/ca.crt');
    const cert = fs.readFileSync('keys/client.crt');
    const key = fs.readFileSync('keys/client.key');
    const kvpair = {
        'private_key': key,
        'cert_chain': cert
    };
    //const credentials = grpc.credentials.createSsl(key, cert, cacert);

    var client = new hello_proto.Greeter('localhost:50051', credentials);
    var user;
    if (process.argv.length >= 3) {
        user = process.argv[2];
    } else {
        user = 'world';
    }
    sayHello(client, user)
}

function sayHello(client, data){
    client.sayHello({name: data}, function(err, response) {
        console.log('Greeting:', response.message);
      });
}
main();