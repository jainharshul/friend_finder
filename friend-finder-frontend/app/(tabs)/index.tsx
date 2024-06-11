import React from 'react';
import { StyleSheet, View, Text, Dimensions } from 'react-native';

const { width } = Dimensions.get('window');

export default function TabOneScreen() {
  return (
    <View style={styles.container}>
      <View style={styles.bigTile}>
        <Text style={styles.title}>Big Tile</Text>
      </View>
      <View style={styles.smallTilesContainer}>
        <View style={styles.smallTile}>
          <Text style={styles.title}>Small Tile 1</Text>
        </View>
        <View style={styles.smallTile}>
          <Text style={styles.title}>Small Tile 2</Text>
        </View>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    padding: 10,
  },
  bigTile: {
    width: '100%',
    height: 200,
    backgroundColor: 'lightgray',
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: 20,
  },
  smallTilesContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    width: '100%',
  },
  smallTile: {
    width: (width - 30) / 2, // Subtracting padding to ensure proper spacing
    height: 150,
    backgroundColor: 'lightblue',
    alignItems: 'center',
    justifyContent: 'center',
  },
  title: {
    fontSize: 20,
    fontWeight: 'bold',
  },
});
