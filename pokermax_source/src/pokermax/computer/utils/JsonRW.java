package pokermax.computer.utils;

import java.io.IOException;
import java.io.InputStream;
import java.util.HashMap;
import java.util.Map;

import com.fasterxml.jackson.databind.ObjectMapper;

public class JsonRW {
	public static HashMap<Integer, Integer> readJSON(String filePath) {
		ObjectMapper objectMapper = new ObjectMapper();
        ClassLoader classLoader = JsonRW.class.getClassLoader();
        InputStream inputStream = classLoader.getResourceAsStream(filePath);
        try {
            @SuppressWarnings("unchecked")
			HashMap<String, Integer> originalMap = objectMapper.readValue(inputStream, HashMap.class);
            HashMap<Integer, Integer> newMap = new HashMap<>();

            for (Map.Entry<String, Integer> entry : originalMap.entrySet()) {
                // Parse string key to integer
                int key = Integer.parseInt(entry.getKey());
                int value = entry.getValue();
                // Put the entry into the new map with integer key
                newMap.put(key, value);
            }

            return newMap;
        } catch (IOException e) {
            e.printStackTrace();
        }
		return null;
    }
}
