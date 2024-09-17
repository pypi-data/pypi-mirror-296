import time
from contextlib import suppress
from typing import Dict, Any, List

import docker
import pydash
from docker.models.containers import Container
from pydantic import BaseModel, Field

import logging

log = logging.getLogger(__name__)

logging.getLogger("docker").setLevel(
	logging.WARNING
)
logging.getLogger("urllib3").setLevel(
	logging.WARNING
)

docker_client = docker.DockerClient(version="auto")

omit_fields = [
	"image_name",
	"image_tag",
	"wait_healthy"
]

ms_in_nanosecond = 1000000
s_in_nanosecond = ms_in_nanosecond * 1000


class LsDockerContainerHealthCheck(BaseModel):
	test: List[str]
	start_period: int | None = s_in_nanosecond * 5
	interval: int | None = s_in_nanosecond * 10
	timeout: int | None = s_in_nanosecond * 10
	retries: int | None = 5

	def __init__(self, /, **data: Any) -> None:
		if "start_period" in data:
			data["start_period"] = s_in_nanosecond * data["start_period"]
		if "interval" in data:
			data["interval"] = s_in_nanosecond * data["interval"]
		if "timeout" in data:
			data["timeout"] = s_in_nanosecond * data["timeout"]
		super().__init__(**data)


class LsDockerContainer(BaseModel):
	image_name: str | None = None
	image_tag: str | None = None
	name: str
	detach: bool | None = True
	ports: Dict[int, int] | None = Field(default_factory=dict)
	extra_hosts: Dict[str, str] = Field(default_factory=dict)
	environment: Dict[str, str] = Field(default_factory=dict)
	wait_healthy: bool = True

	def __init__(self, /, **data: Any) -> None:
		super().__init__(**data)
		if "host.docker.internal" not in self.extra_hosts:
			self.extra_hosts["host.docker.internal"] = "host-gateway"

	@property
	def container(self) -> Container | None:
		# noinspection PyUnresolvedReferences
		with suppress(docker.errors.NotFound):
			container = docker_client.containers.get(self.name)
			return container
		return None

	@property
	def is_running(self) -> bool:
		container = self.container
		return container is not None and container.status == "running"

	def start(self):
		container = self.container
		if container is not None and container.status == "running":
			log.info(f'Container {self.name} already running.')
			return

		log.info(f'Starting container {self.name}...')
		if container is None:
			params = dict(
				image=f"{self.image_name}:{self.image_tag}",
				**pydash.omit(self.model_dump(exclude_none=True), omit_fields),
			)
			docker_client.containers.run(**params)
		else:
			container.start()

		if self.wait_healthy:
			self.wait_container_healthy()

	def wait_container_healthy(self, interval: float = 1.0, max_attempts: int = 30):
		attempt = 0
		container = self.container
		while container.health != "healthy":
			attempt += 1
			if attempt > max_attempts:
				raise Exception("Container not getting healthy in time.")
			container.reload()
			time.sleep(interval)

	def stop(self):
		if self.container is None or self.container.status != "running":
			log.info("Service container not running.")
			return

		log.info("Stopping service container...")
		self.container.stop()

	def remove(self):
		self.container.stop()
		self.container.remove()
