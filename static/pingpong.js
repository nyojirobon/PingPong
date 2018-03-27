$(function(){
  $('body').append('<canvas id="field" width="600" height="400"></canvas>');
  var field = $('canvas')[0];
  var ctx = field.getContext('2d');
  var x;
  var y;
  var dx;
  var dy;
  var speed = [3, -3]
  var ballRadius = 10;
  var paddleHeight = 10;
  var paddleWidth = 100;
  var playerPaddleX;
  var opponentPaddleX;
  var rightPressed = false;
  var leftPressed = false;

  $(document).keydown(function(e){
    if(e.which == 39){
      rightPressed = true;
    }
    else if(e.which == 37){
      leftPressed = true;
    }
  });

  $(document).keyup(function(e){
    if(e.which == 39){
      rightPressed = false;
    }
    else if(e.which == 37){
      leftPressed = false;
    }
  });

  function initialize(){
    x = field.width/2;
    y = field.height/2;
    dx = speed[Math.floor(Math.random() * speed.length)];
    dy = speed[Math.floor(Math.random() * speed.length)];
    playerPaddleX = (field.width - paddleWidth)/2;
    opponentPaddleX = (field.width - paddleWidth)/2;
  }

  function drawBall(){
    ctx.beginPath();
    ctx.arc(x, y, ballRadius, 0, Math.PI*2);
    ctx.fillStyle = "white";
    ctx.fill();
    ctx.closePath();
  }

  function drawPlayerPaddle(){
    ctx.beginPath();
    ctx.rect(playerPaddleX, field.height - paddleHeight, paddleWidth, paddleHeight);
    ctx.fillStyle = "red";
    ctx.fill();
    ctx.closePath();
  }

  function drawOpponentPaddle(){
    ctx.beginPath();
    ctx.rect(opponentPaddleX, 0, paddleWidth, paddleHeight);
    ctx.fillStyle = "black";
    ctx.fill();
    ctx.closePath();
  }

  function drawLine(){
    ctx.beginPath();
    ctx.rect(0, (field.height/2) - 3, field.width, 7);
    ctx.fillStyle = "white";
    ctx.fill();
    ctx.closePath();
  }

  function movePaddles(){
    if(leftPressed && playerPaddleX > 0){
      playerPaddleX -= 10;
    }
    else if(rightPressed && playerPaddleX < field.width - paddleWidth){
      playerPaddleX += 10;
    }
    var action;
    var currentState = {
      "paddle_x" : opponentPaddleX,
      "x" : x,
      "y" : y,
      "dx" : dx,
      "dy" : dy
    };
    var json = JSON.stringify(currentState);
    $.ajax({
      type:'POST',
      url: '/',
      data:json,
      contentType:'application/json',
      dataType:'text',
      async:false,
      success: function(data, dataType){
        action = parseInt(data);
        if(action == 1 && opponentPaddleX > 0){
          opponentPaddleX -= 10;
        }
        else if(action == 2 && opponentPaddleX < field.width - paddleWidth){
          opponentPaddleX += 10
        }
      },
      error: function(jqXHR, textStatus, errorThrown){
        alert("Connection failed.\nNew game will start automatically.");
        console.log(textStatus + ' : ' + errorThrown.message);
        document.location.reload();
        initialize();
      }
    });
  }

  function getAIAction(){

  }

  function moveBall(){
    if(x + dx > field.width - ballRadius || x + dx < ballRadius){
      dx = -dx;
    }

    if(y + dy < ballRadius){
        if(x + ballRadius > opponentPaddleX && x - ballRadius < opponentPaddleX + paddleWidth){
          dy = -dy;
          dy = dy>0? dy+0.3:dy-0.3;
          dx = dx>0? dx+0.3:dx-0.3;
        }
        else{
          alert("You Win!!");
          document.location.reload();
          initialize();
        }
    }
    else if(y + dy > field.height - ballRadius){
      if(x + ballRadius > playerPaddleX && x - ballRadius < playerPaddleX + paddleWidth){
        dy = -dy;
        dy = dy>0? dy+0.3:dy-0.3;
        dx = dx>0? dx+0.3:dx-0.3;
      }
      else{
        alert("You Lose");
        document.location.reload();
        initialize();
      }
    }
    else{
      dy = dy>0? dy-0.001:dy+0.001;
      dx = dx>0? dx-0.001:dx+0.001;
    }
    x += dx;
    y += dy;
  }

  function draw() {
    movePaddles();
    moveBall();
    ctx.clearRect(0, 0, field.width, field.height);
    drawBall();
    drawPlayerPaddle();
    drawOpponentPaddle();
    drawLine();
  }
  initialize();
  setInterval(draw, 10);
});
