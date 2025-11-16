/*
 * Copyright 2012-present the original author or authors.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      https://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package org.springframework.boot.context.config;

import java.io.File;
import java.nio.file.Files;
import java.nio.file.Path;

import org.jspecify.annotations.Nullable;

import org.springframework.boot.origin.Origin;
import org.springframework.core.io.Resource;
import org.springframework.util.Assert;

import com.samedov.annotation.Complexity;
import com.samedov.annotation.Prove;

/**
 * {@link ConfigDataNotFoundException} thrown when a {@link ConfigDataResource} cannot be
 * found.
 *
 * @author Phillip Webb
 * @since 2.4.0
 */
public class ConfigDataResourceNotFoundException extends ConfigDataNotFoundException {

	private final ConfigDataResource resource;

	private final @Nullable ConfigDataLocation location;

	/**
	 * Create a new {@link ConfigDataResourceNotFoundException} instance.
	 * @param resource the resource that could not be found
	 */
	public ConfigDataResourceNotFoundException(ConfigDataResource resource) {
		this(resource, null);
	}

	/**
	 * Create a new {@link ConfigDataResourceNotFoundException} instance.
	 * @param resource the resource that could not be found
	 * @param cause the exception cause
	 */
	public ConfigDataResourceNotFoundException(ConfigDataResource resource, @Nullable Throwable cause) {
		this(resource, null, cause);
	}

	private ConfigDataResourceNotFoundException(ConfigDataResource resource, @Nullable ConfigDataLocation location,
			@Nullable Throwable cause) {
		super(getMessage(resource, location), cause);
		Assert.notNull(resource, "'resource' must not be null");
		this.resource = resource;
		this.location = location;
	}

	/**
	 * Return the resource that could not be found.
	 * @return the resource
	 */
	@Prove(complexity = Complexity.O_1, n = "", count = {})
	public ConfigDataResource getResource() {
		return this.resource;
	}

	/**
	 * Return the original location that was resolved to determine the resource.
	 * @return the location or {@code null} if no location is available
	 */
	@Prove(complexity = Complexity.O_1, n = "", count = {})
	public @Nullable ConfigDataLocation getLocation() {
		return this.location;
	}

	@Override
	@Prove(complexity = Complexity.O_1, n = "", count = {})
	public @Nullable Origin getOrigin() {
		return Origin.from(this.location);
	}

	@Override
	@Prove(complexity = Complexity.O_1, n = "", count = {})
	public String getReferenceDescription() {
		return getReferenceDescription(this.resource, this.location);
	}

	/**
	 * Create a new {@link ConfigDataResourceNotFoundException} instance with a location.
	 * @param location the location to set
	 * @return a new {@link ConfigDataResourceNotFoundException} instance
	 */
	@Prove(complexity = Complexity.O_1, n = "", count = {})
	ConfigDataResourceNotFoundException withLocation(ConfigDataLocation location) {
		return new ConfigDataResourceNotFoundException(this.resource, location, getCause());
	}

	@Prove(complexity = Complexity.O_1, n = "", count = {})
	private static String getMessage(ConfigDataResource resource, @Nullable ConfigDataLocation location) {
		return String.format("Config data %s cannot be found", getReferenceDescription(resource, location));
	}

	@Prove(complexity = Complexity.O_1, n = "", count = {})
	private static String getReferenceDescription(ConfigDataResource resource, @Nullable ConfigDataLocation location) {
		String description = String.format("resource '%s'", resource);
		if (location != null) {
			description += String.format(" via location '%s'", location);
		}
		return description;
	}

	/**
	 * Throw a {@link ConfigDataNotFoundException} if the specified {@link Path} does not
	 * exist.
	 * @param resource the config data resource
	 * @param pathToCheck the path to check
	 */
	@Prove(complexity = Complexity.O_1, n = "", count = {})
	public static void throwIfDoesNotExist(ConfigDataResource resource, Path pathToCheck) {
		throwIfNot(resource, Files.exists(pathToCheck));
	}

	/**
	 * Throw a {@link ConfigDataNotFoundException} if the specified {@link File} does not
	 * exist.
	 * @param resource the config data resource
	 * @param fileToCheck the file to check
	 */
	@Prove(complexity = Complexity.O_1, n = "", count = {})
	public static void throwIfDoesNotExist(ConfigDataResource resource, File fileToCheck) {
		throwIfNot(resource, fileToCheck.exists());
	}

	/**
	 * Throw a {@link ConfigDataNotFoundException} if the specified {@link Resource} does
	 * not exist.
	 * @param resource the config data resource
	 * @param resourceToCheck the resource to check
	 */
	@Prove(complexity = Complexity.O_1, n = "", count = {})
	public static void throwIfDoesNotExist(ConfigDataResource resource, Resource resourceToCheck) {
		throwIfNot(resource, resourceToCheck.exists());
	}

	@Prove(complexity = Complexity.O_1, n = "", count = {})
	private static void throwIfNot(ConfigDataResource resource, boolean check) {
		if (!check) {
			throw new ConfigDataResourceNotFoundException(resource);
		}
	}

}
