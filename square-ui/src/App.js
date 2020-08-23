import React, { Fragment, useRef, useState, useEffect} from 'react';
import {Radio, Button, ButtonGroup} from 'semantic-ui-react'
import 'semantic-ui-css/semantic.min.css';
import './App.css';

const axios = require('axios');

function App() {

  const canvasRef= useRef(null)
  const contextRef = useRef(null)
  const [isDrawing, setIsDrawing] = useState(false)
  const [coordinates, setCoordinates] = useState([])
  const [coordinatesList, setCoordinatesList] = useState([])
  const [timer, setTimer] = useState(0)
  const [appOption, setAppOption] = useState(Boolean(0))
  const [isSquare, setIsSquare] = useState(false);
  const [predictions, setPredictions] = useState([]);

  const [data, setData] = useState({
    "square":[],
    "nsquare":[]
  })

  let canvas;
  var multiplier = 0.5;
  useEffect(()=>{
    const canvas = canvasRef.current;
    canvas.width = window.innerWidth * multiplier;
    canvas.height = window.innerHeight * multiplier;
    canvas.style.width = `${canvas.width}px`;
    canvas.style.height = `${canvas.height}px`;
    const context = canvas.getContext("2d")
    context.scale(multiplier, multiplier)
    context.lineCap = "round"
    context.strokeStyle = "black"
    context.lineWidth = 5
    contextRef.current = context;
  }, [])

  const startDrawing = ({nativeEvent}) => {
    const {offsetX, offsetY} = nativeEvent;

    setTimer(new Date().getTime())

    contextRef.current.beginPath()
    contextRef.current.moveTo(offsetX / multiplier, offsetY / multiplier)
    setIsDrawing(true)
  }

  const finishDrawing = () => {
    contextRef.current.closePath()
    contextRef.current.clearRect(0, 0, window.innerWidth, window.innerHeight);
    appOption ? getPrediction(coordinates) : isSquare ? setData({"square":[...data.square, coordinates], "nsquare":[...data.nsquare]}) : setData({"square":[...data.square], "nsquare":[...data.nsquare, coordinates]})

    setCoordinates([])
    setIsDrawing(false)
  }

  const draw = ({nativeEvent}) => {
    if(!isDrawing){ return }
    const {offsetX, offsetY} = nativeEvent;
    const newData = [(new Date().getTime() - timer), offsetX, offsetY]
    setCoordinates([...coordinates, newData])
    contextRef.current.lineTo(offsetX / multiplier, offsetY / multiplier)
    contextRef.current.stroke()
  }

  const toggleRadio = (e) => {
    setAppOption(!appOption)
  }

  const toggleIsSquare = (e) => {
    setIsSquare(!isSquare)
  }

  const getPrediction = (coordinates) => {
    axios.post(`http://0.0.0.0:8001/predict`, {"data":coordinates})
      .then(res => {setPredictions([...predictions, res.data])})
  }

  const onClickUpload = (e) => {
    if(data.square.length === 0 && data.nsquare.length === 0){
      alert("No data to be uploaded")
      return
    }
    else{
    axios.post(`http://0.0.0.0:8001/retrain/data`, data)
      .then(res => {
        setData({
          "square":[],
          "nsquare":[]
        })
      })
    }
  }

  const onClickRetrain = (e) => {
    axios.post(`http://0.0.0.0:8001/retrain`).then(
      res => {alert("Retraining complete")}
    )
  }

  const onClickResetData = (e) => {
    axios.post(`http://0.0.0.0:8001/reset/data`).then(
      res => {alert("Retraining data removed")}
    )

  }

  const onClickResetModel = (e) => {
    axios.post(`http://0.0.0.0:8001/reset/model`).then(
      res => {alert("Retrained models removed")}
    )
  }


  const onClickResetAll = (e) => {
    axios.post(`http://0.0.0.0:8001/reset`).then(
      res => {alert("Retrained models and retraining data removed")}
    )
  }

  const popSquare = (e) => {
    if (data.square.length >= 1){
      setData({"square":[...data.square.slice(0,-1)], "nsquare":[...data.nsquare]})
    }
  }

  const popNotSquare = (e) => {
    if (data.nsquare.length >= 1){
      setData({"square":[...data.square], "nsquare":[...data.nsquare.slice(0,-1)]})
    }
  }
  return (
    <Fragment>
      <nav className="nav">
        <div><Radio toggle checked={appOption} onClick={e => toggleRadio(e)} />{appOption ? (<h2>Predict</h2>) : (<h2>Retrain</h2>)}
        {appOption ? (<div></div>) : (
            <div className="retrain-buttons">
              <Button onClick={e => onClickUpload(e)} >Push data to retraining</Button>
              <Button onClick={e => onClickRetrain(e)} >Retrain</Button>
            </div>
          )
        }
        </div>
        <ButtonGroup className="reset-group">
          <Button color="red" basic onClick={e => onClickResetData(e)}>Remove uploaded data</Button>
          <Button color="red" basic onClick={e => onClickResetModel(e)}>Remove retrained models</Button>
          <Button color="red" onClick={e => onClickResetAll(data, e)}>Reset All</Button>
        </ButtonGroup>
      </nav>
      <canvas
        style = {{'border': '1px solid black'}}
        onMouseDown={startDrawing}
        onMouseUp={finishDrawing}
        onMouseMove={draw}
        ref={canvasRef}
      />
      {appOption ?
      (<div style={{"padding":"20px"}}>
        <h1>Predictions</h1>
        <ul>
        {appOption ? predictions.slice(0).reverse().map((prediction, index) => <li key={`prediction-${index}`}>{prediction}</li>) : ""}
        </ul>
      </div>):
      (
        <div>
        <div className="toggle-label"><Radio toggle checked={isSquare} onClick={e => toggleIsSquare(e)} /><h3>{isSquare ? "Label: Square"  : "Label: Not Square"}</h3></div>

        <div className="label-counter">
          <ul>
            <li className="list-item"><Button onClick={e => popSquare(e)} >Pop from square list</Button></li>
            <li className="list-item"><Button onClick={e => popNotSquare(e)} >Pop from not square list</Button></li>
            <li className="list-item"><h3>Square: {data["square"].length}</h3></li>
            <li className="list-item"><h3>Not square: {data.nsquare.length}</h3></li>
          </ul>
        </div>
        </div>)
        }
    </Fragment>
  );
}

export default App;
