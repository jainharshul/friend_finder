import React from 'react';
import { Platform, StyleSheet, TextInput, TouchableWithoutFeedback, SafeAreaView, TouchableOpacity } from 'react-native';
import { StatusBar } from 'expo-status-bar';

import { Text, View } from '@/components/Themed';

export default function ModalScreen() {
  return (
    <TouchableWithoutFeedback>
      <SafeAreaView style={styles.container}>
        <View style={styles.formContainer}>
          <View style={styles.inputContainer}>
            <Text style={styles.label}>Title</Text>
            <TextInput
              placeholder='Enter title'
              style={styles.input}
              autoCapitalize='none'
            />
          </View>
          <View style={styles.inputContainer}>
            <Text style={styles.label}>Date</Text>
            <TextInput
              placeholder='Select date'
              style={styles.input}
              autoCapitalize='none'
            />
          </View>
          <View style={styles.inputContainer}>
            <Text style={styles.label}>Time</Text>
            <TextInput
              placeholder='Select time'
              style={styles.input}
              autoCapitalize='none'
            />
          </View>
          <View style={styles.inputContainer}>
            <Text style={styles.label}>Location</Text>
            <TextInput
              placeholder='Enter location'
              style={styles.input}
              autoCapitalize='none'
            />
          </View>
        </View>

        {/* "Invite Friends" Button */}
        <TouchableOpacity style={styles.inviteButton}>
          <Text style={styles.buttonText}>Invite Friends</Text>
        </TouchableOpacity>

        {/* "Add Event" Button */}
        <TouchableOpacity style={styles.addButton}>
          <Text style={styles.buttonText}>Add Event</Text>
        </TouchableOpacity>

        {/* Use a light status bar on iOS to account for the black space above the modal */}
        <StatusBar style={Platform.OS === 'ios' ? 'light' : 'auto'} />
      </SafeAreaView>
    </TouchableWithoutFeedback>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: 'black',
    paddingHorizontal: 20,
  },
  formContainer: {
    width: '80%',
  },
  inputContainer: {
    marginBottom: 20,
  },
  label: {
    marginBottom: 5,
    fontSize: 16,
    fontWeight: 'bold',
    color: 'white', // Adjust text color if needed
  },
  input: {
    width: '100%',
    height: 40,
    borderWidth: 1,
    borderColor: '#ccc',
    borderRadius: 5,
    paddingHorizontal: 10,
    fontSize: 16,
    color: 'white',
  },
  addButton: {
    backgroundColor: 'blue',
    padding: 10,
    borderRadius: 5,
    alignItems: 'center',
    marginTop: 20,
  },
  inviteButton: {
    backgroundColor: 'green',
    padding: 10,
    borderRadius: 5,
    alignItems: 'center',
    marginTop: 10,
  },
  buttonText: {
    color: 'white',
    fontWeight: 'bold',
    fontSize: 16,
  },
});
