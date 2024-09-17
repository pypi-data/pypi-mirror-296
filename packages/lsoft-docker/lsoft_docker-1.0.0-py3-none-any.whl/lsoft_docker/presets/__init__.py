"""
 healthcheck:
      test: echo 'db.runCommand("ping").ok' | mongo mongo:27017/test --quiet 1
      interval: 10s
      timeout: 10s
      retries: 5
"""
from typing import Dict

from pydantic import Field

from lsdocker import LsDockerContainer, LsDockerContainerHealthCheck

mongodb_health_check = LsDockerContainerHealthCheck(
	test=["CMD-SHELL", "echo 'db.runCommand(\"ping\").ok' | mongo mongodb://localhost:27017/ --quiet"],
	start_period=2,
	interval=10,
	timeout=10,
	retries=5,
)


class MongoDBContainer(LsDockerContainer):
	image_name: str | None = 'mongo'
	image_tag: str | None = '4.2'
	name: str | None = 'lsoft-mongodb'
	ports: Dict[int, int] | None = Field(
		default_factory=lambda: dict({
			27017: 32001
		})
	)
	wait_healthy: bool | None = True
	healthcheck: LsDockerContainerHealthCheck | None = mongodb_health_check
