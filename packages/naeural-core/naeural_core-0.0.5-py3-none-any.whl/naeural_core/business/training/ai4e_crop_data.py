# TODO Bleo: WIP
from naeural_core.business.base import CVPluginExecutor as BasePlugin

_CONFIG = {
  **BasePlugin.CONFIG,
  'AI_ENGINE': ['lowres_general_detector'],
  'OBJECT_TYPE': ['person'],

  'ALLOW_EMPTY_INPUTS': True,
  'RUN_WITHOUT_IMAGE': True,
  "CLASSES": None,
  'TRAIN_SIZE': 0.8,

  "FULL_DEBUG_LOG": False,
  "RAW_BACKUP_PERIOD": 30,
  'LOG_FAILED_SAVES': False,
  'FORCE_TERMINATE_COLLECT': False,
  'FORCE_OBJECT_TYPE_BALANCED': False,
  'CLOUD_PATH': 'DATASETS/',
  'OBJECTIVE_NAME': None,
  'REPORT_PERIOD': 10*60,
  'COLLECT_UNTIL': None,
  'POSTPONE_THRESHOLD': 5,

  # These values are only for data transfer purposes
  "DESCRIPTION": "",
  "REWARDS": {},
  "DATASET": {},
  "CREATION_DATE": None,
  "DATA_SOURCES": [],

  'PROCESS_DELAY': 1,
  'MAX_INPUTS_QUEUE_SIZE': 32,

  'VALIDATION_RULES': {
    **BasePlugin.CONFIG['VALIDATION_RULES'],
  },
}

__VER__ = '0.1.0.0'


class Ai4eCropDataOldPlugin(BasePlugin):
  def get_default_labelling_data(self):
    return {
      str(k).lower(): 0 for k in self.get_ds_classes()
    }

  def debug_log(self, msg, **kwargs):
    if self.cfg_full_debug_log:
      self.P(msg, **kwargs)
    return

  def on_init(self):
    super(Ai4eCropDataOldPlugin, self).on_init()
    self.sample_requests = []
    self.voting_status = 0
    self.final_collecting_payload = None
    self._source_names = set()
    self.finished = False
    self.received_input = False
    self.dataset_stats = self.defaultdict(lambda : 0)
    self.total_image_count = 0
    self.dataset_stats_increment = 0
    self.last_increment_time = self.time()
    self.raw_dataset_updates_count = 0
    self.count_saved_by_object_type = self.defaultdict(lambda : 0)
    self.raw_dataset_rel_path = self.os_path.join('raw_datasets', self.cfg_objective_name)
    self.final_dataset_rel_path = self.os_path.join('final_datasets', self.cfg_objective_name)
    self.dataset_abs_path = self.os_path.join(self.get_output_folder(), self.raw_dataset_rel_path)
    self.raw_dataset_set = set()
    self.final_dataset_subdir = {}
    self.final_dataset_stats = {
      'train': 0,
      'dev': 0,
    }
    self.filename_labelling_stats = {}
    self.label_updates_count = 0
    self.started_label_finish = False
    self.gathering_finished = False
    self.raw_dataset_url = None
    self.labels_finished = False
    self.postpone_counter = 0

    self.maybe_load_previous_state()
    return

  def maybe_load_previous_state(self):
    """
    Method for loading the previous state of the plugin.
    """
    self.debug_log('Loading previous state')
    obj = self.persistence_serialization_load()
    if obj is None:
      return
    self.debug_log(f'Loaded previous state: {obj}')
    # endif full debug log
    self.filename_labelling_stats = obj.get('filename_labelling_stats', self.filename_labelling_stats)
    self.dataset_stats = obj.get('dataset_stats', self.dataset_stats)
    self.dataset_stats = self.defaultdict(lambda: 0, self.dataset_stats)
    self.total_image_count = obj.get('total_image_count', self.total_image_count)
    self.total_image_count = max(0, max(sum(self.dataset_stats.values()), self.total_image_count))
    self.label_updates_count = obj.get('label_updates_count', self.label_updates_count)
    self._source_names = set(obj.get('source_names', self._source_names))
    self.started_label_finish = obj.get('started_label_finish', self.started_label_finish)
    self.labels_finished = obj.get('labels_finished', self.labels_finished)
    self.gathering_finished = obj.get('gathering_finished', self.gathering_finished)
    self.raw_dataset_url = obj.get('raw_dataset_url', self.raw_dataset_url)
    self.raw_dataset_set = set(obj.get('raw_dataset_set', self.raw_dataset_set))
    self.count_saved_by_object_type = obj.get('count_saved_by_object_type', self.count_saved_by_object_type)
    self.count_saved_by_object_type = self.defaultdict(lambda: 0, self.count_saved_by_object_type)
    self.final_dataset_subdir = obj.get('final_dataset_subdir', self.final_dataset_subdir)
    self.final_dataset_stats = obj.get('final_dataset_stats', self.final_dataset_stats)
    self.postpone_counter = obj.get('postpone_counter', self.postpone_counter)
    if self.raw_dataset_url is not None:
      self.P(f'Loaded raw dataset URL: {self.raw_dataset_url}')
      self.final_collecting_payload = self.generate_progress_payload(
        return_dict=True,
        url=self.raw_dataset_url,
        path=self.dataset_object_name_raw
      )
    elif self.gathering_finished:
      self.P('Gathering finished, but raw dataset not yet uploaded')

    # endif raw dataset URL is not None
    return

  def maybe_persistance_save(self, force=False):
    """
    Method for saving the plugin state to the disk for persistence.
    """
    to_save = force
    if self.label_updates_count != 0 and self.label_updates_count % self.cfg_label_backup_period == 0:
      to_save = True
    if self.raw_dataset_updates_count != 0 and self.raw_dataset_updates_count % self.cfg_raw_backup_period == 0:
      to_save = True
    if not to_save:
      return
    self.debug_log('Saving plugin state')
    self.persistence_serialization_save(
      obj={
        'filename_labelling_stats': self.filename_labelling_stats,
        'dataset_stats': dict(self.dataset_stats),
        'total_image_count': self.total_image_count,
        'label_updates_count': self.label_updates_count,
        'source_names': list(self._source_names),
        'started_label_finish': self.started_label_finish,
        'labels_finished': self.labels_finished,
        'postpone_counter': self.postpone_counter,
        'gathering_finished': self.gathering_finished,
        'raw_dataset_url': self.raw_dataset_url,
        'raw_dataset_set': list(self.raw_dataset_set),
        'count_saved_by_object_type': dict(self.count_saved_by_object_type),
        'final_dataset_subdir': self.final_dataset_subdir,
        'final_dataset_stats': self.final_dataset_stats,
      },
    )
    return

  def get_job_status(self):
    """
    Method for getting the job status.
    """
    status = "Gathering"
    if self.done_collecting:
      status = "Done Gathering"
    if self.voting_status == 2:
      status = "Labelling"
    if self.labels_finished:
      status = "Done Labelling"
    return status

  def get_dataset_details(self):
    return {
      **self.cfg_dataset,
      'actualSize': self.total_image_count,
    }

  def get_max_size(self):
    dataset_details = self.cfg_dataset
    return dataset_details.get('desiredSize') if dataset_details is not None else None

  def enough_data(self):
    max_size = self.get_max_size()
    if max_size is None:
      return False
    return self.total_image_count >= max_size

  def delay_process(self):
    # Still gathering data
    if not self.gathering_finished:
      return False
    # Done gathering, but not done uploading raw dataset
    if self.raw_dataset_url is None:
      return True
    # Done gathering, done uploading raw dataset, but still labelling
    if not self.started_label_finish:
      return False
    # Done gathering, done uploading raw dataset, done labelling, but final dataset not ready or not uploaded
    if not self.labels_finished:
      return True
    return False

  def get_plugin_loop_resolution(self):
    return self.cfg_plugin_loop_resolution if not self.delay_process() else 1 / 30

  def _create_payload(self, is_status=True, **kwargs):
    additional_kwargs = {} if not is_status else {
      "objective_name": self.cfg_objective_name,
      "rewards": self.cfg_rewards,
      "dataset": self.get_dataset_details(),
      "creation_date": self.cfg_creation_date,
      "data_sources": self.cfg_data_sources,
      "target": self.cfg_object_type,
      "classes": self.get_ds_classes(),
      "description": self.cfg_description,
      "job_status": self.get_job_status()
    }
    return super(Ai4eCropDataOldPlugin, self)._create_payload(
      is_status=is_status,
      **additional_kwargs,
      **kwargs
    )

  def get_collect_until(self):
    """
    Provides possibility to stop collecting data at a certain datetime
    """
    collect_until = self.cfg_collect_until
    if collect_until is not None:
      collect_until = self.datetime.strptime(collect_until, '%Y-%m-%d %H:%M')
    return collect_until

  def get_ds_classes(self):
    classes = self.cfg_classes
    if classes is None:
      classes = self.cfg_object_type
    if not isinstance(classes, (list, dict)):
      classes = [classes]
    if not isinstance(classes, dict):
      classes = {k: k for k in classes}
      return classes
    return classes

  @property
  def collect_until_passed(self):
    collect_until = self.get_collect_until()
    if collect_until is not None:
      return (collect_until - self.datetime.now()).total_seconds() < 0
    return False

  @property
  def dataset_object_name_raw(self):
    return self.os_path.join(self.cfg_cloud_path, self.cfg_objective_name + '_RAW.zip')

  @property
  def dataset_object_name_final(self):
    return self.os_path.join(self.cfg_cloud_path, self.cfg_objective_name + '.zip')

  @property
  def done_collecting(self):
    return self.final_collecting_payload is not None

  def dataset_info_object_filename(self, use_raw=True, include_root=True):
    prefix = self.raw_dataset_rel_path if use_raw else self.final_dataset_rel_path
    if include_root:
      prefix = self.os_path.join(self.get_output_folder(), prefix)
    return self.os_path.join(prefix, 'ADDITIONAL.json')

  """SAVE SECTION"""
  if True:
    def check_if_can_save_object_type(self, object_type):
      """
      Check if the object type can be saved based on the configuration.
      This is used to enforce a balanced dataset if desired.
      Parameters
      ----------
      object_type : str, the object type to check

      Returns
      -------
      bool, whether the object type can be saved
      """
      if not self.cfg_force_object_type_balanced:
        return True

      crt_object_type_count = self.count_saved_by_object_type[object_type]
      can_save = True
      for k in self.cfg_object_type:
        if k == object_type:
          continue

        if crt_object_type_count > self.count_saved_by_object_type[k]:
          can_save = False

      return can_save

    def crop_and_save_one_img(self, np_img, inference, source_name, current_interval):
      """
      Crop and save one image based on the inference data.
      Parameters
      ----------
      np_img : np.ndarray of shape (H, W, C), the image to crop
      inference : dict, the inference data
      source_name : str, the name of the source
      current_interval : str, the current interval

      Returns
      -------
      str, the subdir where the image was saved or None if the save failed
      """
      try:
        self.start_timer('crop_and_save_one_img')
        # Get the top, left, bottom, right positions
        top, left, bottom, right = list(map(lambda x: int(x), inference['TLBR_POS']))
        # Get the object type
        object_type = inference['TYPE']
        # Crop the image
        np_cropped_img = np_img[top:bottom + 1, left:right + 1, :]
        # Get the subdirectory where the image will be saved. This will also be used
        # for the gathering statistics and when generating the final dataset.
        rel_subdir = self.os_path.join(
          str(object_type),
          source_name,
        )
        if current_interval is not None:
          rel_subdir = self.os_path.join(rel_subdir, current_interval)
        # endif interval given
        fname = f'{object_type}_{self.count_saved_by_object_type[object_type]:06d}_{self.now_str(short=True)}'
        fname = self.os_path.join(rel_subdir, fname)
        # Save the image
        success = self.diskapi_save_image_output(
          image=np_cropped_img,
          filename=f'{fname}.jpg',
          subdir=self.raw_dataset_rel_path
        )
        if success:
          self.raw_dataset_set.add(fname)
        else:
          rel_subdir = None
        # endif successful save
        self.stop_timer('crop_and_save_one_img')
      except Exception as e:
        self.stop_timer('crop_and_save_one_img')
        if self.cfg_log_failed_saves:
          self.P(f'Failed save from {source_name} in {current_interval} with exception {e}', color='r')
        return None
      return rel_subdir

    def crop_and_save_all_images(self):
      """
      Crop and save all images from the dataapi.
      Retrieves the images and inferences from the dataapi and saves the images based on the inferences.
      This can also enforce a balanced dataset if configured accordingly.
      Returns
      -------

      """
      dct_imgs = self.dataapi_images()

      for i, np_img in dct_imgs.items():
        # Get the inferences and input metadata
        lst_inferences = self.dataapi_specific_image_instance_inferences(idx=i)
        inp_metadata = self.dataapi_specific_input_metadata(idx=i)
        # Get the source name and current interval
        source_name = inp_metadata.get('SOURCE_STREAM_NAME', self.dataapi_stream_name())
        current_interval = inp_metadata.get('current_interval', 'undefined')
        # Save the source name. Done in order to stop the source when the data gathering is finished.
        # For the moment this is done when the labelling is done. In the future it will be done when the
        # data gathering is finished.
        self._source_names.add(source_name)
        for infer in lst_inferences:
          # Get the object type
          object_type = infer.get('TYPE', None)
          if object_type is None:
            self.P("Inference did not return 'TYPE', cannot save the crop", color='r')
            continue
          # endif no object type
          # Check if the object type can be saved
          if not self.enough_data() and self.check_if_can_save_object_type(object_type):
            # Save the image
            subdir = self.crop_and_save_one_img(
              np_img=np_img, inference=infer, source_name=source_name, current_interval=current_interval
            )
            # In case the image was saved, update the statistics
            if subdir is not None:
              self.count_saved_by_object_type[object_type] += 1
              self.dataset_stats[subdir] += 1
              self.total_image_count += 1
              # Increment the raw dataset counter and maybe backup the state
              self.raw_dataset_updates_count += 1
              self.dataset_stats_increment += 1
              self.maybe_persistance_save()
            # endif successfully saved
          # endif allowed to save
        # endfor inferences
      # endfor images
      return
  """END SAVE SECTION"""

  """COMMANDS SECTION"""
  if True:
    def get_training_subdir(self):
      """
      Get the training subdirectory based on the configured TRAIN_SIZE.
      Returns
      -------
      str, the training subdirectory
      """
      if (self.final_dataset_stats['train'] * self.final_dataset_stats['dev']) == 0:
        if self.final_dataset_stats['train'] == 0:
          return 'train'
        return 'dev'
      # endif no files in train or dev
      train_size = self.cfg_train_size
      train_size = max(0.0, min(1.0, train_size))
      choice = self.np.random.choice([0, 1], p=[1 - train_size, train_size])
      train_subdir = 'dev' if choice == 0 else 'train'
      return train_subdir

    def maybe_copy_file_to_final_dataset(self, filename):
      """
      Method for copying a file to the final dataset in case it is the first
      time it is labeled and the file exists.
      Parameters
      ----------
      filename : str, the filename to check

      Returns
      -------
      int, -1 if the file does not exist or problems occurred,
      0 if the file was already labeled, 1 if the file was copied.
      """
      # Check if the file was already labeled at least once
      if filename in self.filename_labelling_stats.keys():
        self.debug_log(f'File {filename} already copied', color='y')
        return 0
      # Get the raw and final paths
      raw_path = self.os_path.join(self.get_output_folder(), self.raw_dataset_rel_path, f'{filename}.jpg')
      train_subdir = self.get_training_subdir()
      final_path = self.os_path.join(
        self.get_output_folder(), self.final_dataset_rel_path,
        train_subdir, f'{filename}.jpg'
      )
      # Check if the file exists
      if not self.os_path.exists(raw_path):
        self.debug_log(f'File {raw_path} not found', color='r')
        return -1
      # Copy the file
      try:
        self.debug_log(f'Copying file {raw_path} to {final_path}')
        self.diskapi_copy_file(src_path=raw_path, dst_path=final_path)
        self.final_dataset_subdir[filename] = train_subdir
        self.final_dataset_stats[train_subdir] += 1
        return 1
      except Exception as e:
        return -1

    def maybe_handle_datapoint_label(self, datapoint):
      """
      Method for handling the labelling of a datapoint.
      The datapoint has to contain both the filename and the label.
      Parameters
      ----------
      datapoint : dict, the datapoint to label

      Returns
      -------

      """
      if datapoint is None:
        return
      datapoint = {
        k.upper(): v for k, v in datapoint.items()
      }
      filename = datapoint.get('FILENAME', None)
      label = datapoint.get('LABEL', None)
      if label is None or filename is None:
        return
      res = self.maybe_copy_file_to_final_dataset(filename)
      self.debug_log(f'File {filename} copy result: {res}')
      if res != -1:
        self.debug_log(f'File {filename} received label {label}')
        if filename not in self.filename_labelling_stats.keys():
          self.filename_labelling_stats[filename] = self.get_default_labelling_data()
        # endif filename not in stats
        self.filename_labelling_stats[filename][label.lower()] += 1
        self.debug_log(f'{filename} votes:\n{self.filename_labelling_stats[filename]}')
        self.label_updates_count += 1
        self.maybe_persistance_save()
      return

    def finish_labeling(self):
      """
      Method for finishing the labeling process.
      This will compute the label of each file based on the majority vote.
      Returns
      -------

      """
      self.P('Finishing the labelling process')
      self.started_label_finish = True
      self.maybe_persistance_save(force=True)
      self.P('Computing the best label for each file')
      self.debug_log(f'Labelling stats: {self.filename_labelling_stats}')
      for filename in self.filename_labelling_stats.keys():
        label_path = self.os_path.join(self.final_dataset_rel_path, f'{filename}.txt')
        if self.os_path.exists(label_path):
          continue
        best_vote, best_cnt = None, 0
        votes_dict = self.filename_labelling_stats[filename]
        train_subdir = self.final_dataset_subdir[filename]
        for vote, cnt in votes_dict.items():
          if cnt > best_cnt:
            best_vote, best_cnt = vote, cnt
          # endif new best vote
        # endfor votes
        if best_vote is not None:
          self.diskapi_save_file_output(
            data=best_vote,
            filename=f'{filename}.txt',
            subdir=self.os_path.join(self.final_dataset_rel_path, train_subdir)
          )
        # endif best vote
      # endfor filenames
      # TODO: zip dataset and upload for start of training
      self.P('Archive the final dataset')
      zip_path = self.diskapi_zip_dir(self.os_path.join(self.get_output_folder(), self.final_dataset_rel_path))
      self.P(f'Uploading the final dataset to {self.dataset_object_name_final}')
      self.upload_file(
        file_path=zip_path,
        target_path=self.dataset_object_name_final,
        force_upload=True,
      )
      self.labels_finished = True
      self.maybe_persistance_save(force=True)
      return

    def maybe_copy_additional_files(self):
      """
      Method for copying the additional files to the final dataset.
      """
      final_ds_additional_path = self.dataset_info_object_filename(use_raw=False)
      self.P(f'Copying additional files to {final_ds_additional_path} from {self.dataset_info_object_filename(use_raw=True)}')
      if self.os_path.exists(final_ds_additional_path):
        return
      raw_ds_additional_path = self.dataset_info_object_filename(use_raw=True)
      if not self.os_path.exists(raw_ds_additional_path):
        return
      self.diskapi_copy_file(src_path=raw_ds_additional_path, dst_path=final_ds_additional_path)
      return

    def maybe_start_voting(self):
      if self.voting_status == 1:
        config = {
          'TYPE': 'VOID',
          'NAME': 'VOTING_now',
          'PLUGINS': [
            {
              'SIGNATURE': 'label_voting',
              'INSTANCES': [
                {
                  'INSTANCE_ID': 'voting',
                }
              ]
            }
          ]
        }
        self.P('Starting the voting process')
        self.cmdapi_start_pipeline(
          config=config
        )
        self.voting_status = 2
      return

    def sample_filename(self):
      return self.np.random.choice(list(self.raw_dataset_set)) if len(self.raw_dataset_set) > 0 else None

    def filename_to_path(self, filename):
      return self.os_path.join(
        self.get_output_folder(), self.raw_dataset_rel_path, f'{filename}.jpg'
      )

    def maybe_process_sample_requests(self, data, **kwargs):
      """
      Method for processing the sample requests received as commands.
      Parameters
      ----------
      data : dict, the data to handle
      kwargs : dict, additional keyword arguments

      Returns
      -------
      bool, whether the command is a request or not
      """
      is_request = False
      request_id = data.get('REQUEST_ID')
      response_kwargs = {
        'request_id': request_id
      }
      sample_filename = data.get('FILENAME')
      sample_request = data.get('SAMPLE', False)
      if sample_request:
        response_kwargs['sample_filename'] = self.sample_filename()
        is_request = True
      elif sample_filename is not None:
        response_kwargs['sample_path'] = self.filename_to_path(sample_filename)
        response_kwargs['IMG'] = self.diskapi_load_image(
          folder='output',
          filename=f'{sample_filename}.jpg',
          subdir=self.raw_dataset_rel_path
        )
        is_request = True
      if is_request:
        self.add_payload(
          self._create_payload(
            is_status=False,
            **response_kwargs
          )
        )
      return is_request

    # TODO: change `_on_command`s to 'on_command' in all the plugins
    def on_command(self, data, **kwargs):
      """
      Method for handling the command data.
      Parameters
      ----------
      data : dict, the data to handle
      kwargs : dict, additional keyword arguments

      Returns
      -------

      """
      self.P(f'Got command {data}')
      # In case the command is a sample request, register it and return
      if self.maybe_process_sample_requests(data, **kwargs):
        return
      datapoint = data.get("DATAPOINT")
      self.maybe_copy_additional_files()
      self.maybe_handle_datapoint_label(datapoint)
      start_voting = data.get('START_VOTING', False)
      if start_voting:
        self.voting_status = 1
      finish_labelling = data.get("FINISH_LABELLING", False)
      if finish_labelling:
        self.finish_labeling()
      # endif finish labelling
      return
  """END COMMANDS SECTION"""

  def generate_progress_payload(self, return_dict=False, add_crop_speed=False, **kwargs):
    payload_kwargs = {
      **kwargs,
      'counts': self.dataset_stats,
    }
    if add_crop_speed:
      payload_kwargs['crop_increment'] = self.dataset_stats_increment
      payload_kwargs['duration'] = self.time() - self.last_increment_time
      payload_kwargs['crop_speed'] = self.dataset_stats_increment / payload_kwargs['duration']
      self.last_increment_time = self.time()
      self.dataset_stats_increment = 0
    return payload_kwargs if return_dict else self._create_payload(**payload_kwargs)

  def archive_and_upload_ds(self):
    classes_data = {
      'classes': self.get_ds_classes(),
      'name': self.cfg_objective_name,
    }
    classes_path = self.diskapi_save_json_to_output(
      dct=classes_data, filename=self.dataset_info_object_filename(include_root=False)
    )
    fn_zip = self.diskapi_zip_dir(self.dataset_abs_path)
    ds_url, _ = self.upload_file(
      file_path=fn_zip,
      target_path=self.dataset_object_name_raw,
      force_upload=True
    )
    self.diskapi_delete_file(fn_zip)
    return ds_url

  def stop_gather(self):
    self.P(f'Stopping all the other data sources: {self._source_names}')
    self.cmdapi_stop_current_stream()
    for s in self._source_names:
      self.cmdapi_stop_other_stream_on_current_box(s)
    self.finished = True
    return

  def get_labelling_payload(self):
    return self._create_payload(
      label_counts=len(list(self.filename_labelling_stats.keys())),
      **self.final_collecting_payload
    )

  def finalise_collecting_process(self):
    if self.raw_dataset_url is not None:
      self.P(f'Raw dataset already uploaded at {self.raw_dataset_url}')
      return
    self.gathering_finished = True
    ds_url = self.archive_and_upload_ds()
    payload_kwargs = {
      'url': ds_url, 'path': self.dataset_object_name_raw,
    }
    self.final_collecting_payload = self.generate_progress_payload(return_dict=True, **payload_kwargs)
    self.add_payload(self.get_labelling_payload())
    self.raw_dataset_url = ds_url
    self.maybe_persistance_save(force=True)
    return

  def _process(self):
    self.maybe_start_voting()
    # TODO: test data gathering when other pipelines are running
    # We should only gather from the specified streams
    # Step 1: If gathering not finished and input available, crop and save all images.
    if not self.gathering_finished and self.dataapi_received_input():
      self.crop_and_save_all_images()
      self.received_input = True

    payload = None
    # Step 2: If report period passed, generate progress payload if still collecting
    # or generate labelling payload if the data is being labeled. This is only relevant
    # if the raw dataset was uploaded and is being annotated.
    if self.time() - self.last_payload_time >= self.cfg_report_period:
      payload = self.get_labelling_payload() if self.done_collecting else self.generate_progress_payload(
        add_crop_speed=True
      )

    # Step 3: If no more data gathering is needed, but it was not yet finished,
    # finalise the process and start sending labelling payload.
    if (self.collect_until_passed or self.cfg_force_terminate_collect or self.enough_data()) and not self.done_collecting:
      self.finalise_collecting_process()
      payload = None
    # endif no more data gathering needed

    # Step 4: If the finishing of the labelling started, but not yet finished,
    # retry the labelling process.
    if not self.labels_finished and self.started_label_finish:
      self.finish_labeling()
    # endif the labelling process was started, but not yet finished

    # Step 5: If the data was labeled further processing will be postponed
    # one time for the upload command to be received.
    # After that the plugin will stop the data sources and the current pipeline.
    if self.labels_finished:
      if self.postpone_counter < self.cfg_postpone_threshold:
        self.P(f'Postponing the labelling finish for the upload command to be received'
               f'({self.postpone_counter + 1}/{self.cfg_postpone_threshold})')
        self.postpone_counter += 1
      elif not self.finished:
        self.stop_gather()
      payload = None
    # endif data was labeled
    return payload


class Ai4eCropDataPlugin(BasePlugin):

  def debug_log(self, msg, **kwargs):
    if self.cfg_full_debug_log:
      self.P(msg, **kwargs)
    return

  def on_init(self):
    super(Ai4eCropDataPlugin, self).on_init()
    self.label_updates_count = 0
    self.raw_dataset_updates_count = 0
    self.raw_dataset_rel_path = self.os_path.join('raw_datasets', self.cfg_objective_name)
    self.dataset_stats_increment = 0
    self.last_increment_time = self.time()

    self.gathering_finished = False
    self.source_names = set()

    self.dataset_abs_path = self.os_path.join(self.get_output_folder(), self.raw_dataset_rel_path)
    self.total_image_count = 0
    self.raw_dataset_set = set()
    self.count_saved_by_object_type = self.defaultdict(lambda: 0)
    self.dataset_stats = self.defaultdict(lambda: 0)

    self.voting_status = 0
    self.postpone_counter = 0
    self.finished = False
    self.maybe_load_previous_state()
    return

  def maybe_load_previous_state(self):
    """
    Method for loading the previous state of the plugin.
    Returns
    """
    self.debug_log('Loading previous state')
    obj = self.persistence_serialization_load()
    if obj is None:
      return
    self.debug_log(f'Loaded previous state: {obj}')

    self.gathering_finished = obj.get('gathering_finished', self.gathering_finished)
    self.source_names = set(obj.get('source_names', self.source_names))

    self.total_image_count = obj.get('total_image_count', self.total_image_count)
    self.raw_dataset_set = set(obj.get('raw_dataset_set', self.raw_dataset_set))
    self.count_saved_by_object_type = obj.get('count_saved_by_object_type', self.count_saved_by_object_type)
    self.count_saved_by_object_type = self.defaultdict(lambda: 0, self.count_saved_by_object_type)
    self.dataset_stats = obj.get('dataset_stats', self.dataset_stats)
    self.dataset_stats = self.defaultdict(lambda: 0, self.dataset_stats)

    return

  def maybe_persistence_save(self, force=False):
    """
    Method for saving the plugin state to the disk for persistence.
    """
    to_save = force
    if self.raw_dataset_updates_count != 0 and self.raw_dataset_updates_count % self.cfg_raw_backup_period == 0:
      to_save = True
    if not to_save:
      return
    self.debug_log('Saving plugin state')
    self.persistence_serialization_save(
      obj={
        'gathering_finished': self.gathering_finished,
        'source_names': list(self.source_names),

        'total_image_count': self.total_image_count,
        'raw_dataset_set': list(self.raw_dataset_set),
        'count_saved_by_object_type': dict(self.count_saved_by_object_type),
        'dataset_stats': dict(self.dataset_stats),
      }
    )
    return

  """UTILS SECTION"""
  if True:
    @property
    def dataset_object_name_raw(self):
      return self.os_path.join(self.cfg_cloud_path, self.cfg_objective_name + '_RAW.zip')

    def get_collect_until(self):
      """
      Provides possibility to stop collecting data at a certain datetime
      """
      collect_until = self.cfg_collect_until
      if collect_until is not None:
        collect_until = self.datetime.strptime(collect_until, '%Y-%m-%d %H:%M')
      return collect_until

    @property
    def collect_until_passed(self):
      collect_until = self.get_collect_until()
      if collect_until is not None:
        return (collect_until - self.datetime.now()).total_seconds() < 0
      return False

    def get_ds_classes(self):
      classes = self.cfg_classes
      if classes is None:
        classes = self.cfg_object_type
      if not isinstance(classes, (list, dict)):
        classes = [classes]
      if not isinstance(classes, dict):
        classes = {k: k for k in classes}
        return classes
      return classes

    def get_job_status(self):
      """
      Method for getting the job status.
      """
      status = "Gathering"
      if not self.need_data():
        status = "Done Gathering"
      if self.voting_status == 2:
        status = "Publishing"
      return status

    def get_dataset_details(self):
      return {
        **self.cfg_dataset,
        'actualSize': self.total_image_count,
      }

    def get_max_size(self):
      dataset_details = self.cfg_dataset
      return dataset_details.get('desiredSize') if dataset_details is not None else None

    def enough_data(self):
      max_size = self.get_max_size()
      if max_size is None:
        return False
      return self.total_image_count >= max_size

    def need_data(self):
      return not self.enough_data() and not self.collect_until_passed and not self.cfg_force_terminate_collect
  """END UTILS SECTION"""

  """PAYLOAD SECTION"""
  if True:
    def _create_payload(self, is_status=True, **kwargs):
      additional_kwargs = {} if not is_status else {
        "objective_name": self.cfg_objective_name,
        "rewards": self.cfg_rewards,
        "dataset": self.get_dataset_details(),
        "creation_date": self.cfg_creation_date,
        "data_sources": self.cfg_data_sources,
        "target": self.cfg_object_type,
        "classes": self.get_ds_classes(),
        "description": self.cfg_description,
        "job_status": self.get_job_status()
      }
      return super(Ai4eCropDataPlugin, self)._create_payload(
        is_status=is_status,
        **additional_kwargs,
        **kwargs
      )

    def generate_progress_payload(self, return_dict=False, add_crop_speed=False, **kwargs):
      payload_kwargs = {
        **kwargs,
        'counts': self.dataset_stats,
        'counts_per_class': self.count_saved_by_object_type,
      }
      if add_crop_speed:
        payload_kwargs['crop_increment'] = self.dataset_stats_increment
        duration = self.time() - self.last_increment_time
        payload_kwargs['duration'] = duration
        payload_kwargs['crop_speed'] = self.dataset_stats_increment / duration if duration > 0 else 0
        self.last_increment_time = self.time()
        self.dataset_stats_increment = 0
      return payload_kwargs if return_dict else self._create_payload(**payload_kwargs)
  """END PAYLOAD SECTION"""

  """COMMANDS SECTION"""
  if True:
    def start_upload_plugin(self):
      self.P(f'Uploading the raw dataset to {self.dataset_object_name_raw}')
      config = {
        'TYPE': 'VOID',
        'NAME': f'UPLOAD_{self.get_instance_id()}',
        'PLUGINS': [{
          'SIGNATURE': 'minio_upload_dataset',
          'INSTANCES': [{
            'INSTANCE_ID': self.get_instance_id(),
            'DATASET_OBJECT_NAME': self.dataset_object_name_raw,
            'DATASET_LOCAL_PATH': self.dataset_abs_path,
            'IS_RAW': True
          }]
        }]
      }
      self.cmdapi_start_pipeline(config=config)
      return
    def maybe_start_voting(self):
      if self.voting_status == 1:
        self.maybe_persistence_save(force=True)
        self.start_upload_plugin()
        # start upload plugin for the dataset
        # make the voting pipeline of type minio dataset
        config = {
          'TYPE': 'minio_dataset',
          'STREAM_CONFIG_METADATA': {
            'DATASET_OBJECT_NAME': self.dataset_object_name_raw,
          },
          'NAME': f'label_{self.get_instance_id()}',
          'PLUGINS': [
            {
              'SIGNATURE': 'ai4e_label_data',
              'INSTANCES': [
                {
                  # TODO: complete this
                  'INSTANCE_ID': self.get_instance_id(),

                  'CLASSES': self.get_ds_classes(),
                  'TRAIN_SIZE': self.cfg_train_size,

                  'OBJECTIVE_NAME': self.cfg_objective_name,
                  'REWARDS': self.cfg_rewards,
                  'DATASET': self.get_dataset_details(),
                  'CREATION_DATE': self.cfg_creation_date,
                  'DESCRIPTION': self.cfg_description,
                  'REPORT_PERIOD': self.cfg_report_period
                }
              ]
            }
          ]
        }
        self.P('Starting the voting process')
        self.cmdapi_start_pipeline(
          config=config
        )
        self.voting_status = 2
      # endif voting needs to start
      return

    def stop_gather(self):
      self.P(f'Stopping all the other data sources: {self.source_names}')
      self.cmdapi_stop_current_stream()
      for s in self.source_names:
        self.cmdapi_stop_other_stream_on_current_box(s)
      self.finished = True
      return

    def sample_filename(self):
      return self.np.random.choice(list(self.raw_dataset_set)) if len(self.raw_dataset_set) > 0 else None

    def filename_to_path(self, filename):
      return self.os_path.join(
        self.get_output_folder(), self.raw_dataset_rel_path, f'{filename}.jpg'
      )

    def maybe_process_sample_requests(self, data, **kwargs):
      """
      Method for processing the sample requests received as commands.
      Parameters
      ----------
      data : dict, the data to handle
      kwargs : dict, additional keyword arguments

      Returns
      -------
      bool, whether the command is a request or not
      """
      is_request = False
      request_id = data.get('REQUEST_ID')
      if request_id is None:
        return is_request
      response_kwargs = {
        'request_id': request_id
      }
      sample_filename = data.get('FILENAME')
      chosen_filename = self.sample_filename() if sample_filename is None else sample_filename
      # if filename not provided, a random one will be selected
      sample_request = data.get('SAMPLE', False)
      img = self.diskapi_load_image(
        folder='output',
        filename=f'{chosen_filename}.jpg',
        subdir=self.raw_dataset_rel_path
      )
      if sample_request:
        response_kwargs['sample_filename'] = chosen_filename
        response_kwargs['IMG'] = img
        is_request = True
      elif sample_filename is not None:
        response_kwargs['sample_path'] = self.filename_to_path(chosen_filename)
        response_kwargs['IMG'] = img
        is_request = True
      if is_request:
        self.add_payload(
          self._create_payload(
            is_status=False,
            **response_kwargs
          )
        )
      return is_request

    def on_command(self, data, **kwargs):
      """
      Method for handling the command data.
      Parameters
      ----------
      data : dict, the data to handle
      kwargs : dict, additional keyword arguments

      Returns
      -------

      """
      self.P(f'Got command {data}')
      # In case the command is a sample request, register it and return
      if self.maybe_process_sample_requests(data, **kwargs):
        return
      start_voting = data.get('START_VOTING', False)
      if start_voting and self.voting_status == 0:
        self.P(f'Requesting the start of the voting process')
        self.voting_status = 1
      return

  """END COMMANDS SECTION"""

  """SAVE SECTION"""
  if True:
    def check_if_can_save_object_type(self, object_type):
      """
      Check if the object type can be saved based on the configuration.
      This is used to enforce a balanced dataset if desired.
      Parameters
      ----------
      object_type : str, the object type to check

      Returns
      -------
      bool, whether the object type can be saved
      """
      if not self.cfg_force_object_type_balanced:
        return True

      crt_object_type_count = self.count_saved_by_object_type[object_type]
      can_save = True
      for k in self.cfg_object_type:
        if k == object_type:
          continue

        if crt_object_type_count > self.count_saved_by_object_type[k]:
          can_save = False

      return can_save

    def crop_and_save_one_img(self, np_img, inference, source_name, current_interval):
      """
      Crop and save one image based on the inference data.
      Parameters
      ----------
      np_img : np.ndarray of shape (H, W, C), the image to crop
      inference : dict, the inference data
      source_name : str, the name of the source
      current_interval : str, the current interval

      Returns
      -------
      str, the subdir where the image was saved or None if the save failed
      """
      try:
        self.start_timer('crop_and_save_one_img')
        # Get the top, left, bottom, right positions
        top, left, bottom, right = list(map(lambda x: int(x), inference['TLBR_POS']))
        # Get the object type
        object_type = inference['TYPE']
        # Crop the image
        np_cropped_img = np_img[top:bottom + 1, left:right + 1, :]
        # Get the subdirectory where the image will be saved. This will also be used
        # for the gathering statistics and when generating the final dataset.
        rel_subdir = self.os_path.join(
          str(object_type),
          source_name,
        )
        if current_interval is not None:
          rel_subdir = self.os_path.join(rel_subdir, current_interval)
        # endif interval given
        fname = f'{object_type}_{self.count_saved_by_object_type[object_type]:06d}_{self.now_str(short=True)}'
        fname = self.os_path.join(rel_subdir, fname)
        # Save the image
        success = self.diskapi_save_image_output(
          image=np_cropped_img,
          filename=f'{fname}.jpg',
          subdir=self.raw_dataset_rel_path
        )
        if success:
          self.raw_dataset_set.add(fname)
        else:
          rel_subdir = None
        # endif successful save
        self.stop_timer('crop_and_save_one_img')
      except Exception as e:
        self.stop_timer('crop_and_save_one_img')
        if self.cfg_log_failed_saves:
          self.P(f'Failed save from {source_name} in {current_interval} with exception {e}', color='r')
        return None
      return rel_subdir

    def crop_and_save_all_images(self):
      """
      Crop and save all images from the dataapi.
      Retrieves the images and inferences from the dataapi and saves the images based on the inferences.
      This can also enforce a balanced dataset if configured accordingly.
      Returns
      -------

      """
      dct_imgs = self.dataapi_images()

      for i, np_img in dct_imgs.items():
        # Get the inferences and input metadata
        lst_inferences = self.dataapi_specific_image_instance_inferences(idx=i)
        inp_metadata = self.dataapi_specific_input_metadata(idx=i)
        # Get the source name and current interval
        source_name = inp_metadata.get('SOURCE_STREAM_NAME', self.dataapi_stream_name())
        current_interval = inp_metadata.get('current_interval', 'undefined')
        # Save the source name. Done in order to stop the source when the data gathering is finished.
        # For the moment this is done when the labelling is done. In the future it will be done when the
        # data gathering is finished.
        self.source_names.add(source_name)
        for infer in lst_inferences:
          # Get the object type
          object_type = infer.get('TYPE', None)
          if object_type is None:
            self.P("Inference did not return 'TYPE', cannot save the crop", color='r')
            continue
          # endif no object type
          # Check if the object type can be saved
          if not self.enough_data() and self.check_if_can_save_object_type(object_type):
            # Save the image
            subdir = self.crop_and_save_one_img(
              np_img=np_img, inference=infer, source_name=source_name, current_interval=current_interval
            )
            # In case the image was saved, update the statistics
            if subdir is not None:
              self.count_saved_by_object_type[object_type] += 1
              self.dataset_stats[subdir] += 1
              self.total_image_count += 1
              # Increment the raw dataset counter and maybe backup the state
              self.raw_dataset_updates_count += 1
              self.dataset_stats_increment += 1
              self.maybe_persistence_save()
            # endif successfully saved
          # endif allowed to save
        # endfor inferences
      # endfor images
      return
  """END SAVE SECTION"""

  def _process(self):
    # Step 1: Start the voting process if not already started in case
    # it was requested by a command.
    self.maybe_start_voting()
    # TODO: test data gathering when other pipelines are running
    # We should only gather from the specified streams
    # Step 2: If gathering not finished and input available, crop and save all images.
    if self.need_data() and self.dataapi_received_input():
      self.crop_and_save_all_images()
    # endif need data and input available

    payload = None
    # Step 3: If report period passed, generate progress payload
    if self.time() - self.last_payload_time >= self.cfg_report_period:
      payload = self.generate_progress_payload(add_crop_speed=True)
    # endif report period passed

    # Step 4: If the voting started, there is no need
    # for this plugin or the data sources to continue.
    if self.voting_status == 2:
      if self.postpone_counter < self.cfg_postpone_threshold:
        self.P(f'Postponing the labelling finish for the upload command to be received'
               f'({self.postpone_counter + 1}/{self.cfg_postpone_threshold})')
        self.postpone_counter += 1
      elif not self.finished:
        self.stop_gather()
      # endif postpone counter not reached
    # endif voting started

    return payload


