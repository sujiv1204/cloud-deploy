from flask import Flask, jsonify
import random
import time

app = Flask(__name__)


@app.route('/')
def home():
    return "Compute Engine is running. Hit /process-image for heavy load."


@app.route('/process-image')
def process_image():
    """
    Simulates a heavy Computer Vision operation (2D Convolution).
    This uses pure Python nested loops to intentionally max out CPU utilization.
    """
    start_time = time.time()

    # Simulate a 400x400 grayscale image grid
    image_size = 600
    image = [[random.random() for _ in range(image_size)]
             for _ in range(image_size)]

    # Simulate a 3x3 filter kernel (e.g., used for edge detection/stitching prep)
    kernel = [[random.random() for _ in range(3)] for _ in range(3)]

    # Output matrix
    result = [[0 for _ in range(image_size - 2)]
              for _ in range(image_size - 2)]

    # O(N^2 * K^2) complexity: Massive CPU stress via nested loops
    for i in range(image_size - 2):
        for j in range(image_size - 2):
            val = 0
            for ki in range(3):
                for kj in range(3):
                    val += image[i+ki][j+kj] * kernel[ki][kj]
            result[i][j] = val

    processing_time = time.time() - start_time

    return jsonify({
        "status": "success",
        "message": "2D Image Convolution complete.",
        "pixels_processed": (image_size - 2) ** 2,
        "processing_time_seconds": round(processing_time, 4)
    })


if __name__ == '__main__':
    # Threaded=True ensures the server attempts to process concurrent oha requests
    app.run(host='0.0.0.0', port=80, threaded=True)
