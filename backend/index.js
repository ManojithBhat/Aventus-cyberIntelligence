
import express from 'express';
import bodyParser from 'body-parser';
import cors from 'cors';
import { spawn } from 'child_process';
const app = express();
const port = 8080;

app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(cors());


app.get('/endpoint/:id', (req, res) => {
  const receivedUrl= req.params.id; 
  console.log('Received URL:', receivedUrl);
  let result = '';
  let responseSent = false; // Flag to track if response has been sent

  const pythonProcess = spawn('python', ['app.py', receivedUrl]);
  
  pythonProcess.stdout.on('data', (data) => {
      result += data.toString();
      //console.log(result);
  });
   
  pythonProcess.stderr.on('data', (data) => {
      console.error(`stderr: ${data}`);
      if (!responseSent) { // Check if response has already been sent
          responseSent = true;
          res.status(500).send('Error occurred while running Python script');
      }
  });
    
  pythonProcess.on('close', (code) => {
      if (!responseSent) { // Check if response has already been sent
          responseSent = true;
          
          console.log('before splitting',result)
          const predictionAndScore = result.split(' ');

          const prediction = predictionAndScore[0];
          const score = predictionAndScore[3];
          console.log('score is ',score,typeof(score));

          const responseObject = {
            prediction: prediction,
            score: score
          };

          console.log(responseObject)

          if (code === 0) {
            //console.log(result)
              if(prediction === "0") {
                  res.json(responseObject);
              } else {
                  res.json(responseObject);
              }
          } else {
              res.status(500).send('Python script exited with an error');
          }
      }
  });
});


app.listen(port, () => {
    console.log(`Server is running at http://localhost:${port}`);
});
