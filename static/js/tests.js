document.addEventListener('DOMContentLoaded', () => {
    // API Connection Test
    const testApiConnectionBtn = document.getElementById('test-api-connection');
    const apiConnectionResult = document.getElementById('api-connection-result');
    
    testApiConnectionBtn.addEventListener('click', async () => {
        apiConnectionResult.textContent = 'Testing...';
        
        try {
            const response = await fetch('/api/health');
            const data = await response.json();
            
            if (response.ok && data.status === 'ok') {
                apiConnectionResult.textContent = '✅ Success: API is running';
                apiConnectionResult.style.color = 'green';
            } else {
                apiConnectionResult.textContent = `❌ Failed: ${data.message || 'Unknown error'}`;
                apiConnectionResult.style.color = 'red';
            }
        } catch (error) {
            apiConnectionResult.textContent = `❌ Failed: ${error.message}`;
            apiConnectionResult.style.color = 'red';
        }
    });
    
    // Database Connection Test
    const testDbConnectionBtn = document.getElementById('test-db-connection');
    const dbConnectionResult = document.getElementById('db-connection-result');
    
    testDbConnectionBtn.addEventListener('click', async () => {
        dbConnectionResult.textContent = 'Testing...';
        
        try {
            // We'll implement this endpoint later when we add database functionality
            const response = await fetch('/api/database-status');
            
            if (!response.ok) {
                dbConnectionResult.textContent = `❌ Failed: ${response.statusText}`;
                dbConnectionResult.style.color = 'red';
                return;
            }
            
            const data = await response.json();
            
            if (data.status === 'connected') {
                dbConnectionResult.textContent = '✅ Success: Database is connected';
                dbConnectionResult.style.color = 'green';
            } else {
                dbConnectionResult.textContent = `❌ Failed: ${data.message || 'Unknown error'}`;
                dbConnectionResult.style.color = 'red';
            }
        } catch (error) {
            dbConnectionResult.textContent = `❌ Failed: ${error.message}`;
            dbConnectionResult.style.color = 'red';
        }
    });
    
    // LLM API Test
    const testLlmApiBtn = document.getElementById('test-llm-api');
    const llmApiResult = document.getElementById('llm-api-result');
    
    testLlmApiBtn.addEventListener('click', async () => {
        llmApiResult.textContent = 'Testing...';
        
        try {
            // We'll implement this endpoint later when we add LLM API functionality
            const response = await fetch('/api/llm-test');
            
            if (!response.ok) {
                llmApiResult.textContent = `❌ Failed: ${response.statusText}`;
                llmApiResult.style.color = 'red';
                return;
            }
            
            const data = await response.json();
            
            if (data.status === 'success') {
                llmApiResult.textContent = '✅ Success: LLM API is working';
                llmApiResult.style.color = 'green';
            } else {
                llmApiResult.textContent = `❌ Failed: ${data.message || 'Unknown error'}`;
                llmApiResult.style.color = 'red';
            }
        } catch (error) {
            llmApiResult.textContent = `❌ Failed: ${error.message}`;
            llmApiResult.style.color = 'red';
        }
    });
});