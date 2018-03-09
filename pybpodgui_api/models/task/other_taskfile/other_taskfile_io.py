from .other_taskfile_base import OtherTaskFileBase
import os

class OtherTaskFileIO(OtherTaskFileBase):

	def save(self, repository):

		repository.add_file( self.filepath , self.name)

		data = {}
		data['execute']  = self.execute
		data['detached'] = self.detached
		repository['other-files'][self.name] = data

		self.filepath = os.path.join(repository.path, self.name)
        

	def load(self, repository):
		data = repository.get('other-files', {}).get(self.name, {})
		self.execute  = data.get('execute', False)
		self.detached = data.get('detached', False)
		