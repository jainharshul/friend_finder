import React from 'react';
import { View, Text, StyleSheet } from 'react-native';

export default function Tile({ title, date, time, location, style }) {
  return (
    <View style={[styles.container, style]}>
      <Text style={styles.title}>{title}</Text>
      {date && <Text style={styles.info}>{date}</Text>}
      {time && <Text style={styles.info}>{time}</Text>}
      {location && <Text style={styles.info}>{location}</Text>}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    borderWidth: 1,
    borderColor: 'black',
    padding: 10,
    borderRadius: 5,
  },
  title: {
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 5,
  },
  info: {
    fontSize: 16,
  },
});
