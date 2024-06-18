import { StyleSheet, ImageBackground } from 'react-native';
import map from '../../assets/map.png'

import { Text, View } from '@/components/Themed';

export default function TabTwoScreen() {
  return (
    <ImageBackground
      source={map}
      style={styles.backgroundImage}
    >
      <View style={styles.overlay}>
        
      </View>
    </ImageBackground>
  );
}

const styles = StyleSheet.create({
  backgroundImage: {
    flex: 1,
    resizeMode: 'cover', // or 'stretch' to stretch the image to fit the screen
    justifyContent: 'center', // Center the content within the ImageBackground
  },
  overlay: {
    flex: 1,
    backgroundColor: 'rgba(0, 0, 0, 0)', // Optional: add a semi-transparent overlay
    justifyContent: 'center',
    alignItems: 'center',
  },
  container: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
  },
  title: {
    fontSize: 20,
    fontWeight: 'bold',
  },
  separator: {
    marginVertical: 30,
    height: 1,
    width: '80%',
  },
});
