package com.test.maps.repository;

import java.util.Date;
import java.util.List;
import java.util.Optional;
import java.util.UUID;

import com.test.maps.model.Maps;

import org.springframework.data.repository.CrudRepository;
import org.springframework.data.rest.core.annotation.RepositoryRestResource;
import org.springframework.data.repository.query.Param;

@RepositoryRestResource
public interface MapsRepository extends CrudRepository<Maps, UUID> {
    List<Maps> findByUrlContaining(@Param("url") String url);
    Optional<Maps> findById(UUID id);
    List<Maps> findByDateGreaterThan(@Param("date") Date date);
    Maps findByDate(Date date);
    List<Maps> findByMetaContains(String meta);


}