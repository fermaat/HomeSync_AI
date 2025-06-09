import React, { useState, useEffect } from 'react';
import {
  StyleSheet,
  Text,
  View,
  Button,
  Image,
  TextInput,
  ActivityIndicator,
  ScrollView,
  Alert,
  Platform,
} from 'react-native';
import * as ImagePicker from 'expo-image-picker';
import axios from 'axios';

import { LOCAL_IP } from '@env';
//const LOCAL_IP = LOCAL_IP // || '192.168.1.116'; // Reemplaza con tu IP local si no está definida en .env
const BACKEND_URL = `http://${LOCAL_IP}:8000/api/v1`;

export default function App() {
  const [selectedImageUri, setSelectedImageUri] = useState(null);
  const [selectedImageBase64, setSelectedImageBase64] = useState(null);
  const [processingImage, setProcessingImage] = useState(false);
  const [imageResponse, setImageResponse] = useState(null);

  const [voiceCommand, setVoiceCommand] = useState('');
  const [processingVoice, setProcessingVoice] = useState(false);
  const [voiceResponse, setVoiceResponse] = useState(null);

  // Visual logs for debugging
  const [debugLogs, setDebugLogs] = useState([]);

  // log function to keep track of debug messages
  const addDebugLog = (message) => {
    const timestamp = new Date().toLocaleTimeString();
    setDebugLogs(prev => [...prev.slice(-4), `[${timestamp}] ${message}`]); // keep last 5 logs
    console.log(message); // Also send to console just in case
  };

  useEffect(() => {
    (async () => {
      if (Platform.OS !== 'web') {
        const { status } = await ImagePicker.requestCameraPermissionsAsync();
        if (status !== 'granted') {
          Alert.alert('Permissions needed', 'We need permissions to access the camera.');
        }
      }
    })();
  }, []);

  const pickImage = async () => {
    let result;
    try {
      addDebugLog('🔍 Launching image selection...');
      
      if (Platform.OS === 'web') {
        result = await ImagePicker.launchImageLibraryAsync({
          mediaTypes: ImagePicker.MediaTypeOptions.Images,
          allowsEditing: true,
          aspect: [4, 3],
          quality: 0.7,
          base64: true,
        });
      } else {
        result = await ImagePicker.launchCameraAsync({
          mediaTypes: ImagePicker.MediaTypeOptions.Images,
          allowsEditing: true,
          aspect: [4, 3],
          quality: 0.7,
          base64: true,
        });
      }

      if (!result.canceled) {
        addDebugLog('✅ Image selected successfully ');
        setSelectedImageUri(result.assets[0].uri);
        setSelectedImageBase64(result.assets[0].base64);
        
        const base64Length = result.assets[0].base64 ? result.assets[0].base64.length : 0;
        addDebugLog(`📏 Base64 length: ${base64Length}`);
        addDebugLog(`🔤 Base64 preview: ${result.assets[0].base64 ? result.assets[0].base64.substring(0, 50) + '...' : 'null'}`);
        
        setImageResponse(null);
      } else {
        addDebugLog('❌ Image selection canceled');
      }
    } catch (error) {
      addDebugLog(`❌ Error selecting image: ${error.message}`);
      Alert.alert("Error", "Image could not be selected: " + error.message);
    }
  };

  const processTicket = async () => {
    if (!selectedImageBase64) {
      addDebugLog('❌ No Base64 image to process');
      Alert.alert('Error', 'Please select or take a photo of the ticket first to process it.');
      return;
    }

    addDebugLog(`🚀 Starting processing. Base64 length: ${selectedImageBase64.length}`);
    addDebugLog(`🔗 Backend URL: ${BACKEND_URL}/process_ticket`);

    setProcessingImage(true);
    setImageResponse(null);

    const requestData = {
      image_base64: selectedImageBase64, // CAMBIADO: imagen_base64 -> image_base64
      prompt_gemini: "Extract the products, quantities, unit prices, and totals from this purchase ticket. Give me the result in JSON format. Include the purchase date if you find it.",
    };

    addDebugLog(`📦 Data types to send: image_base64=${typeof selectedImageBase64}, prompt_gemini=${typeof requestData.prompt_gemini}`);

    try {
      addDebugLog('📡 Sending request to backend...');

      const response = await axios.post(`${BACKEND_URL}/process_ticket`, requestData, {
        headers: {
          'Content-Type': 'application/json',
        },
      });

      addDebugLog('✅ Response received from backend');
      setImageResponse(`Ticket response:\n${JSON.stringify(response.data, null, 2)}`);

    } catch (error) {
      addDebugLog(`❌ Backend error: ${error.response?.status} - ${error.response?.statusText}`);
      addDebugLog(`❌ Error details: ${JSON.stringify(error.response?.data)}`);

      const errorMessage = error.response?.data?.detail || error.message || "Unknown error";
      setImageResponse(`Error: ${errorMessage}`);
      Alert.alert('Error', `An error occurred while processing the ticket: ${errorMessage}`);
    } finally {
      setProcessingImage(false);
      addDebugLog('🏁 Processing finished');
    }
  };

  const sendVoiceCommand = async () => {
    if (!voiceCommand.trim()) {
      Alert.alert('Error', 'Please enter a voice command.');
      return;
    }

    setProcessingVoice(true);
    setVoiceResponse(null);

    try {
      const response = await axios.post(`${BACKEND_URL}/process_voice_command`, {
        command_text: voiceCommand,
      });
      setVoiceResponse(`Voice command response:\n${JSON.stringify(response.data, null, 2)}`);
    } catch (error) {
      console.error('Error sending voice command:', error.response?.data || error.message);
      setVoiceResponse(`Error: ${error.response?.data?.detail || error.message}`);
      Alert.alert('Error', 'An error occurred while processing the voice command. Check the console and your backend.');
    } finally {
      setProcessingVoice(false);
    }
  };

  return (
    <ScrollView contentContainerStyle={styles.container}>
      <Text style={styles.title}>HomeSync AI - Demo IA</Text>

      {/* Debug logs pannel */}
      {/* {debugLogs.length > 0 && (
        <View style={styles.debugPanel}>
          <Text style={styles.debugTitle}>🐛 Debug Logs:</Text>
          {debugLogs.map((log, index) => (
            <Text key={index} style={styles.debugText}>{log}</Text>
          ))}
          <Button 
            title="Clean Logs" 
            onPress={() => setDebugLogs([])}
            color="#ff6b6b"
          />
        </View>
      )} */}

      {/* Sección de Procesamiento de Tickets */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>1. Process Ticket</Text>
        <Button title="Take/Select Ticket Photo" onPress={pickImage} />
        {selectedImageUri && (
          <Image source={{ uri: selectedImageUri }} style={styles.imagePreview} />
        )}
        <Button
          title="Send Ticket to AI (Gemini)"
          onPress={processTicket}
          disabled={!selectedImageUri || processingImage}
        />
        {processingImage && <ActivityIndicator size="large" color="#0000ff" style={styles.spinner} />}
        {imageResponse && (
          <View style={styles.responseBox}>
            <Text style={styles.responseText}>{imageResponse}</Text>
          </View>
        )}
      </View>

      <View style={styles.separator} />

      {/* Sección de Comandos de Voz (simulados) */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>2. Voice Command (Text)</Text>
        <TextInput
          style={styles.textInput}
          placeholder="E.g: What do we need to buy?"
          value={voiceCommand}
          onChangeText={setVoiceCommand}
        />
        <Button
          title="Send Command to AI"
          onPress={sendVoiceCommand}
          disabled={!voiceCommand.trim() || processingVoice}
        />
        {processingVoice && <ActivityIndicator size="large" color="#0000ff" style={styles.spinner} />}
        {voiceResponse && (
          <View style={styles.responseBox}>
            <Text style={styles.responseText}>{voiceResponse}</Text>
          </View>
        )}
      </View>

      <View style={styles.separator} />

      <Text style={styles.footerText}>
        Make sure your backend is running at "{BACKEND_URL}"
        and that your mobile/emulator is on the same Wi-Fi network.
      </Text>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flexGrow: 1,
    backgroundColor: '#f5f5f5',
    alignItems: 'center',
    padding: 20,
    paddingTop: 50,
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    marginBottom: 30,
    color: '#333',
  },
  // NEW: Styles for the debug panel
  debugPanel: {
    width: '100%',
    backgroundColor: '#2d3748',
    borderRadius: 8,
    padding: 15,
    marginBottom: 20,
  },
  debugTitle: {
    color: '#f7fafc',
    fontSize: 16,
    fontWeight: 'bold',
    marginBottom: 10,
  },
  debugText: {
    color: '#e2e8f0',
    fontSize: 12,
    fontFamily: Platform.OS === 'ios' ? 'Menlo' : 'monospace',
    marginBottom: 5,
  },
  section: {
    width: '100%',
    backgroundColor: '#fff',
    borderRadius: 10,
    padding: 20,
    marginBottom: 20,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  sectionTitle: {
    fontSize: 20,
    fontWeight: '600',
    marginBottom: 15,
    color: '#555',
  },
  imagePreview: {
    width: '100%',
    height: 200,
    resizeMode: 'contain',
    marginVertical: 15,
    borderColor: '#eee',
    borderWidth: 1,
    borderRadius: 5,
  },
  textInput: {
    height: 50,
    borderColor: '#ddd',
    borderWidth: 1,
    borderRadius: 5,
    paddingHorizontal: 15,
    marginBottom: 15,
    fontSize: 16,
  },
  spinner: {
    marginVertical: 15,
  },
  responseBox: {
    backgroundColor: '#eef',
    borderRadius: 8,
    padding: 15,
    marginTop: 15,
    borderLeftWidth: 4,
    borderLeftColor: '#007bff',
  },
  responseText: {
    fontSize: 14,
    fontFamily: Platform.OS === 'ios' ? 'Menlo' : 'monospace',
    color: '#333',
  },
  separator: {
    height: 1,
    width: '80%',
    backgroundColor: '#ccc',
    marginVertical: 30,
  },
  footerText: {
    fontSize: 12,
    color: '#777',
    textAlign: 'center',
    marginTop: 20,
  }
});