#include <torch/extension.h>

__device__ int countTransitions(int* neighbors) {
    int count = 0;
    for (int i = 0; i < 8; i++) {
        if (neighbors[i] == 0 && neighbors[(i + 1) % 8] == 1) {
            count++;
        }
    }
    return count;
}

__global__ void zhangSuenIteration(int* image, int* marker, int width, int height, int iter, bool* hasChanged) {
    int x = blockIdx.x * blockDim.x + threadIdx.x;
    int y = blockIdx.y * blockDim.y + threadIdx.y;

    if (x <= 0 || y <= 0 || x >= width - 1 || y >= height - 1)
        return;

    int P1 = image[y * width + x];
    if (P1 != 1)
        return;

    // Get the 8 neighbors of the pixel
    int P2 = image[(y - 1) * width + x];
    int P3 = image[(y - 1) * width + (x + 1)];
    int P4 = image[y * width + (x + 1)];
    int P5 = image[(y + 1) * width + (x + 1)];
    int P6 = image[(y + 1) * width + x];
    int P7 = image[(y + 1) * width + (x - 1)];
    int P8 = image[y * width + (x - 1)];
    int P9 = image[(y - 1) * width + (x - 1)];

    // Create the neighbors array
    int neighbors[8] = { P2, P3, P4, P5, P6, P7, P8, P9 };

    // Calculate the sum of neighbors (B)
    int B = P2 + P3 + P4 + P5 + P6 + P7 + P8 + P9;

    // Count the transitions (A)
    int A = countTransitions(neighbors);

    // Conditions for the first sub-iteration or second sub-iteration
    int m1, m2;
    if (iter == 0) {
        m1 = P2 * P4 * P6;
        m2 = P4 * P6 * P8;
    } else {
        m1 = P2 * P4 * P8;
        m2 = P2 * P6 * P8;
    }

    // Mark pixel for removal
    if (A == 1 && B >= 2 && B <= 6 && m1 == 0 && m2 == 0) {
        marker[y * width + x] = 1;
        *hasChanged = true; // Mark that a change occurred
    }
}

__global__ void applyMarker(int* image, int* marker, int width, int height) {
    int x = blockIdx.x * blockDim.x + threadIdx.x;
    int y = blockIdx.y * blockDim.y + threadIdx.y;

    if (x <= 0 || y <= 0 || x >= width - 1 || y >= height - 1)
        return;

    if (marker[y * width + x] == 1) {
        image[y * width + x] = 0;
    }
}

torch::Tensor skeletonize(torch::Tensor image) {
    // Convert to binary (0 and 1) if it's not already
    image = (image > 0).to(torch::kInt32);

    int width = image.size(1);
    int height = image.size(0);

    auto marker = torch::zeros_like(image, image.options());

    dim3 threadsPerBlock(16, 16);
    dim3 numBlocks((width + threadsPerBlock.x - 1) / threadsPerBlock.x,
                   (height + threadsPerBlock.y - 1) / threadsPerBlock.y);

    auto d_image = image.data_ptr<int>();
    auto d_marker = marker.data_ptr<int>();

    bool hasChanged = true;
    bool* d_hasChanged;
    cudaMalloc(&d_hasChanged, sizeof(bool));

    while (hasChanged) {
        hasChanged = false;
        cudaMemcpy(d_hasChanged, &hasChanged, sizeof(bool), cudaMemcpyHostToDevice);

        // Reset marker
        cudaMemset(d_marker, 0, width * height * sizeof(int));

        // Run the first sub-iteration (iter = 0)
        zhangSuenIteration<<<numBlocks, threadsPerBlock>>>(d_image, d_marker, width, height, 0, d_hasChanged);
        cudaDeviceSynchronize();

        // Apply the marker to remove marked pixels
        applyMarker<<<numBlocks, threadsPerBlock>>>(d_image, d_marker, width, height);
        cudaDeviceSynchronize();

        // Run the second sub-iteration (iter = 1)
        zhangSuenIteration<<<numBlocks, threadsPerBlock>>>(d_image, d_marker, width, height, 1, d_hasChanged);
        cudaDeviceSynchronize();

        // Apply the marker to remove marked pixels
        applyMarker<<<numBlocks, threadsPerBlock>>>(d_image, d_marker, width, height);
        cudaDeviceSynchronize();

        // Check if changes were made in this iteration
        cudaMemcpy(&hasChanged, d_hasChanged, sizeof(bool), cudaMemcpyDeviceToHost);
    }

    cudaFree(d_hasChanged);

    // Convert the image back to uint8 (0 and 255) if necessary
    return image.to(torch::kUInt8) * 255;
}

PYBIND11_MODULE(TORCH_EXTENSION_NAME, m) {
    m.def("skeletonize", &skeletonize, "Zhang-Suen thinning algorithm (CUDA)");
}
