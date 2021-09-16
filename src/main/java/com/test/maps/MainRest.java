package com.test.maps;


import java.sql.Date;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import java.util.UUID;

import com.test.maps.model.Maps;
import com.test.maps.repository.MapsRepository;

import org.springframework.beans.factory.annotation.Autowired;


import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/maps") // actual API endpoint structure could be better laid out, will research this later.
public class MainRest {


	@Autowired
	MapsRepository mapsRepository;


	// Returns everything in database
	@GetMapping("/all")
	public ResponseEntity<List<Maps>> getAllMaps(@RequestParam(required = false) String url) {
		try {
			List<Maps> maps = new ArrayList<Maps>();

			if (url == null)
				mapsRepository.findAll().forEach(maps::add);
			else
				mapsRepository.findByUrlContaining(url).forEach(maps::add);

			if (maps.isEmpty()) {
				return new ResponseEntity<>(HttpStatus.NO_CONTENT);
			}

			return new ResponseEntity<>(maps, HttpStatus.OK);
		} catch (Exception e) {
			return new ResponseEntity<>(null, HttpStatus.INTERNAL_SERVER_ERROR);
		}
	}

	// Returns based on id
	@GetMapping("/id/{id}")
	public ResponseEntity<Maps> getMapsById(@PathVariable("id") UUID id) {
		Optional<Maps> mapsData = mapsRepository.findById(id);

		if (mapsData.isPresent()) {
			return new ResponseEntity<>(mapsData.get(), HttpStatus.OK);
		} else {
			return new ResponseEntity<>(HttpStatus.NOT_FOUND);
		}
	}

	// returns based on a date 
	@GetMapping("/date/{date}")
	public ResponseEntity<List<Maps>> getMapsByDate(@PathVariable("date") String mydate) {
		try {		
			List<Maps> mapsData  = new ArrayList<Maps>();
			
			//Pageable page = PageRequest.of(0, 10);
			/*
			if (date.isEmpty()){
				mapsRepository.findTop10ByDate("0", page).forEach(mapsData::add);
			} else {
			} */
			mapsRepository.findByDateGreaterThan(Date.valueOf(mydate)).forEach(mapsData::add);
			
			

			return new ResponseEntity<>(mapsData, HttpStatus.OK);

		} catch (Exception e) {
			return new ResponseEntity<>(null, HttpStatus.INTERNAL_SERVER_ERROR);
		}
	}

	// Find based on a search of meta content
	@GetMapping("/meta/{keyWord}")
	public ResponseEntity<List<Maps>> getMapsByMetaKeyword(@PathVariable String keyWord) {
			List<Maps> mapsData = new ArrayList<Maps>();
			mapsRepository.findByMetaContains(keyWord).forEach(mapsData::add);
			return new ResponseEntity<>(mapsData, HttpStatus.OK);
	}

	
	// Add an entry into database
	@PostMapping("/new")
	public void addEntry(@RequestBody Maps maps) {
			mapsRepository.save(maps);
	}

}
