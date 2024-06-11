import React, { useState } from 'react';
import { StyleSheet, View, Dimensions, ScrollView } from 'react-native';
import Tile from '../../components/Tile';

const { width } = Dimensions.get('window');

export default function TabOneScreen() {
  const [tiles, setTiles] = useState([
    { id: 1, title: 'Big Tile', type: 'big', date: 'June 10, 2024', time: '10:00 AM', location: 'New York' },
    { id: 2, title: 'Side Event', type: 'small', date: 'June 12, 2024', time: '2:00 PM', location: 'Los Angeles' },
    { id: 3, title: 'Balls', type: 'small', date: 'June 15, 2024', time: '6:00 PM', location: 'San Francisco' },
  ]);

  const bigTile = tiles.find(tile => tile.type === 'big');

  return (
    <View style={styles.container}>
      <ScrollView contentContainerStyle={styles.scrollContainer}>
        <View style={styles.bigTile}>
          {bigTile && (
            <Tile
              title="Main Event"
              date={bigTile.date}
              time={bigTile.time}
              location={bigTile.location}
              style={styles.bigTileStyle}
            />
          )}
        </View>
        <View style={styles.smallTilesContainer}>
          {tiles.filter(tile => tile.type === 'small').map(tile => (
            <View key={tile.id} style={styles.smallTile}>
              <Tile
                title={tile.title}
                date={tile.date}
                time={tile.time}
                location={tile.location}
                style={styles.smallTileStyle}
              />
            </View>
          ))}
        </View>
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  scrollContainer: {
    padding: 10,
    alignItems: 'center',
  },
  bigTile: {
    width: '100%',
    marginBottom: 20,
  },
  smallTilesContainer: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'space-between',
    width: '100%',
  },
  smallTile: {
    width: (width - 30) / 2,
    marginBottom: 20,
  },
  bigTileStyle: {
    width: '100%',
    height: 200,
    backgroundColor: 'white',
  },
  smallTileStyle: {
    width: '100%',
    height: 150,
    backgroundColor: 'white',
  },
});
