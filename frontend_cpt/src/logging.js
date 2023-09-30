import "./log.css";
import { useRef, useEffect } from "react";

function Log({ onClick, url, date }) {
	const videoRef = useRef(null);
	const canvasRef = useRef(null);

	useEffect(() => {
		const video = videoRef.current;

		video.addEventListener("loadeddata", () => {
			console.log("Video loaded:", url);
			video.currentTime = 1;
		});

		video.addEventListener("seeked", () => {
			console.log("Video seeked:", url);
			const canvas = canvasRef.current;
			const ctx = canvas.getContext("2d");
			ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
		});
	}, [url]);

	useEffect(() => {
		console.log("Component rendered with date:", date);
	}, [date]);

	return (
		<div onClick={onClick} className="log">
			<video ref={videoRef} src={url} style={{ display: "none" }}></video>
			<canvas ref={canvasRef} width="100" height="100"></canvas>
			<div className="details">
				<h3>Person Motion Detected</h3>
				<p>{date}</p>
			</div>
		</div>
	);
}

export default Log;
