// app/login.tsx
import React from 'react';
import { View, SafeAreaView, Text, TextInput, Button, StyleSheet, TouchableWithoutFeedback, Keyboard } from 'react-native';
import { Link } from 'expo-router';
import { Colors, Styles } from '../styles'

export default function LoginRegisterScreen({ }) {
  return (
    <TouchableWithoutFeedback onPress={Keyboard.dismiss}>
      <View style={styles.container}>
        <Text style={styles.title}>ETA</Text>
        <TextInput style={styles.input} placeholder="Username" />
        <TextInput style={styles.input} placeholder="Password" secureTextEntry />
        <Link replace href="(tabs)" asChild>
          <Button title="Login" />
        </Link>
        <Link replace href="(tabs)" asChild>
          <Button title="Register" />
        </Link>
      </View>
    </TouchableWithoutFeedback >
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 20,
    backgroundColor: Colors.black,
  },
  title: {
    fontSize: 24,
    marginBottom: 20,
    color: Colors.white,
  },
  input: {
    width: '100%',
    padding: 10,
    marginVertical: 10,
    borderWidth: 1,
    borderColor: Colors.white,
    borderRadius: 5,
    color: Colors.white
  },
});
