var app = require('express')();
    http = require('http').Server(app),
    io = require('socket.io')(http),
    bodyParser     = require('body-parser');

/***** Configure Express app with *****/
app.use(bodyParser.json());
app.use(bodyParser.urlencoded());
//app.use(cookieParser());
//app.use(xmlparser());

io.on('connection', function(socket){
  console.log('a user connected');
  socket.on('disconnect', function(){
    console.log('user disconnected');
  });
});

http.listen(3000, function(){
  console.log('listening on *:3000');
});

app.post('/api/myfarog/battle/update/', function(req, res){
    
    // TODO(Keith): Add validation
    var msg         = req.body.msg;
    var battle_id   = req.body.battle_id
    
    // TODO(Keith): Only send to the users in the battle being updated
    //io.sockets.in(battle_id).emit('battle update', msg);
    io.sockets.emit('battle update', msg);
    
    res.send({"success":true, "body": msg } );

});