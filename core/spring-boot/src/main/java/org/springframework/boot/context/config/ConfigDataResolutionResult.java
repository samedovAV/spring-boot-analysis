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

import com.samedov.annotation.Complexity;
import com.samedov.annotation.Prove;

/**
 * Result returned from {@link ConfigDataLocationResolvers} containing both the
 * {@link ConfigDataResource} and the original {@link ConfigDataLocation}.
 *
 * @author Phillip Webb
 */
class ConfigDataResolutionResult {

	private final ConfigDataLocation location;

	private final ConfigDataResource resource;

	private final boolean profileSpecific;

	ConfigDataResolutionResult(ConfigDataLocation location, ConfigDataResource resource, boolean profileSpecific) {
		this.location = location;
		this.resource = resource;
		this.profileSpecific = profileSpecific;
	}

	@Prove(complexity = Complexity.O_1, n = "", count = {})
	ConfigDataLocation getLocation() {
		return this.location;
	}

	@Prove(complexity = Complexity.O_1, n = "", count = {})
	ConfigDataResource getResource() {
		return this.resource;
	}

	@Prove(complexity = Complexity.O_1, n = "", count = {})
	boolean isProfileSpecific() {
		return this.profileSpecific;
	}

}
