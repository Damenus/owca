import os
import yaml
import shutil

letter = 'g'
path = '/home/damdar/serenity/workload-collocation-agent/examples/kubernetes/workloads/memcached-2pod/'
name = 'wss-2pod-' + letter + '-'
test_path = path + 'test' + letter + '/'

shutil.rmtree(test_path)
os.makedirs(test_path)

f = open(test_path + "kustomization.yaml", "a")
f.write("bases:" + "\n")
f.close()

for i in range(1, 36):
#for i in range(1000, 30000, 1000):

    folder_path = test_path + name + str(i)
    try:
        os.makedirs(folder_path)
    except OSError as e:
        print("ERROR: " + e)

    f = open(test_path + "kustomization.yaml", "a")
    f.write("- " + name + str(i) + "\n")
    f.close()

    kustomization = dict(
        nameSuffix= '-' + name + str(i),
        bases=[
            '../../base'
        ],
        commonLabels=dict(
            app='memcached-mutilate-' + name + str(i),
        ),
        configMapGenerator=[
            dict(
                name='mutilate',
                behavior='merge',
                literals=[
                    # 'load_records='+str(int(12000000/i * 100)),  # 2->8
                    # 'records='+str(int(12000000/i * 100)),
                    'load_records=' + str(int(12000000 / i / 11 * 100)),  # 2->8
                    'records=' + str(int(12000000 / i / 11 * 100 )),
                    'valuesize='+str(int(1000)),
                    'qps='+str(int(0)),
                    'threads=1',
                    'connections=1',
                    'update=0.2',  # 80/20 or 50/50
                ],
            ),
        ],
        patchesStrategicMerge=[
            "resources1.yaml",
            "resources2.yaml"
        ],
    )

    resources1 = dict(
        apiVersion='apps/v1',
        kind='StatefulSet',
        metadata=dict(
            name='memcached'
        ),
        spec=dict(
            template=dict(
                spec=dict(
                    containers=[
                        dict(
                            name='memcached',
                            resources=dict(
                                requests=dict(
                                    cpu=1,
                                    memory=str(int((180-i)/i)) + 'G'
                                    # memory=str(int(1500 / 6)) + 'G'
                                ),
                                limits=dict(
                                    cpu=1,
                                    memory=str(int((180-i)/i)) + 'G'
                                    # memory=str(int(1500 / 6)) + 'G'
                                )
                            ),
                        ),
                    ],
                ),
            ),
        ),
    )

    resources2 = dict(
        apiVersion='apps/v1',
        kind='StatefulSet',
        metadata=dict(
            name='mutilate'
        ),
        spec=dict(
            template=dict(
                spec=dict(
                    containers=[
                        dict(
                            name='mutilate',
                            resources=dict(
                                requests=dict(
                                    cpu=1,
                                    memory='1G'
                                ),
                                limits=dict(
                                    cpu=1,
                                    memory='1G'
                                )
                            ),
                        ),
                    ],
                ),
            ),
        ),
    )

    with open(folder_path + '/kustomization.yaml', 'w') as outfile:
        yaml.dump(kustomization, outfile, default_flow_style=False)
    with open(folder_path + '/resources1.yaml', 'w') as outfile:
        yaml.dump(resources1, outfile, default_flow_style=False)
    with open(folder_path + '/resources2.yaml', 'w') as outfile:
        yaml.dump(resources2, outfile, default_flow_style=False)



# TEST 3 17/03/2020
    # kustomization = dict(
    #     nameSuffix= '-' + name + str(i),
    #     bases=[
    #         '../../base'
    #     ],
    #     commonLabels=dict(
    #         app='memcached-mutilate-' + name + str(i),
    #     ),
    #     configMapGenerator=[
    #         dict(
    #             name='mutilate',
    #             behavior='merge',
    #             literals=[
    #                 'load_records='+str(int(13000000/i * 2)),
    #                 'records='+str(int(13000000/i * 2)),
    #                 'valuesize='+str(int(100000 / 2)),
    #                 'qps='+str(12000),
    #                 'threads=1',
    #                 'connections=1'
    #             ],
    #         ),
    #     ],
    #     patchesStrategicMerge=[
    #         "resources.yaml"
    #     ],
    # )
    #
    # resources = dict(
    #     apiVersion='apps/v1',
    #     kind='StatefulSet',
    #     metadata=dict(
    #         name='memcached-mutilate'
    #     ),
    #     spec=dict(
    #         template=dict(
    #             spec=dict(
    #                 containers=[
    #                     dict(
    #                         name='memcached',
    #                         resources=dict(
    #                             requests=dict(
    #                                 cpu=1,
    #                                 memory=str(1500/i) + 'G'
    #                             ),
    #                             limits=dict(
    #                                 cpu=1,
    #                                 memory=str(1500/i) + 'G'
    #                             )
    #                         ),
    #                     ),
    #                     dict(
    #                         name='mutilate',
    #                         resources=dict(
    #                             requests=dict(
    #                                 cpu=1,
    #                                 memory='1G'
    #                             ),
    #                             limits=dict(
    #                                 cpu=1,
    #                                 memory='1G'
    #                             )
    #                         ),
    #                     ),
    #                 ],
    #             ),
    #         ),
    #     ),
    # )


    # TEST
    #         configMapGenerator=[
#             dict(
#                 name='mutilate',
#                 behavior='merge',
#                 literals=[
#                     'load_records='+str(int(13000000/35 * 2)),
#                     'records='+str(int(13000000/35 * 2)),
#                     'valuesize='+str(int(100000 / 2)),
#                     'qps='+str(int(12000/35*i)),
#                     'threads=1',
#                     'connections=1',
#                     #'update=0.2',  # 80/20 or 50/50
#                 ],
#             ),
#         ],