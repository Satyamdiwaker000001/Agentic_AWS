const API_BASE_URL = 'http://127.0.0.1:8000';

export const uploadFileForChunking = async (file, method) => {
  const formData = new FormData();
  formData.append('file', file);

  const endpoint = method === 'fixed' ? '/chunk/fixed' : '/chunk/recursive';
  
  try {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      method: 'POST',
      body: formData,
      // No Content-Type header needed; fetch sets it automatically with the boundary for FormData
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || 'Failed to process file');
    }

    return await response.json();
  } catch (error) {
    throw new Error(error.message || 'An error occurred while connecting to the API');
  }
};
