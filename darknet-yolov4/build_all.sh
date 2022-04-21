#get bash logs
export BUILDKIT_PROGRESS=plain

#source ../env.sh
source ./image_config.sh
echo "IMAGE_PREFIX=$IMAGE_PREFIX"
echo "IMAGE_VERSION=$IMAGE_VERSION"


IMAGE_OS=nvidia/cuda:11.2.2-cudnn8-devel-ubuntu20.04
IMAGE_BASE=${IMAGE_PREFIX}_base_${IMAGE_VERSION}
IMAGE_INFERENCE=${IMAGE_PREFIX}_inference_${IMAGE_VERSION}
IMAGE_TRAIN=${IMAGE_PREFIX}_train_${IMAGE_VERSION}

echo ${IMAGE_BASE}
echo ${IMAGE_INFERENCE}
echo ${IMAGE_TRAIN}
#
#cd base-dockers
#
##1
#cd ../base-dockers
#parent_image=$IMAGE_OS
#build_image=$IMAGE_BASE
#str_build="docker build  --build-arg BASE_CONTAINER=$parent_image  -f Dockerfile -t $build_image ."
#echo "======  $str_build START======"
#$str_build
#retVal=$?
#if [ $retVal -ne 0 ]; then
#    echo "======  $str_build . ERROR======"
#    exit $retVal
#fi
#echo "======  $str_build . END======\n\n\n"
#sleep 5
#
#
##2
#cd ../inference;
#parent_image=$IMAGE_BASE
#build_image=$IMAGE_INFERENCE
#str_build="docker build  --build-arg BASE_CONTAINER=$parent_image  -f Dockerfile -t $build_image ."
#echo "======  $str_build START======"
#$str_build
#retVal=$?
#if [ $retVal -ne 0 ]; then
#    echo "======  $str_build . ERROR======"
#    exit $retVal
#fi
#echo "======  $str_build . END======\n\n\n"
#sleep 5
#
#
##3
#cd ../train
#parent_image=$IMAGE_BASE
#build_image=$IMAGE_TRAIN
#str_build="docker build  --build-arg BASE_CONTAINER=$parent_image  -f Dockerfile -t $build_image ."
#echo "======  $str_build START======"
#$str_build
#retVal=$?
#if [ $retVal -ne 0 ]; then
#    echo "======  $str_build . ERROR======"
#    exit $retVal
#fi
#echo "======  $str_build . END======\n\n\n"
#sleep 5
#
#
#
#
#echo ${IMAGE_BASE}
#echo ${IMAGE_INFERENCE}
#echo ${IMAGE_TRAIN}
#
#
#
##6
#echo "======  docker push $IMAGE_BASE START======"
#docker push $IMAGE_BASE
#retVal=$?
#if [ $retVal -ne 0 ]; then
#    echo "======  docker push $IMAGE_BASE ERROR======"
#    exit $retVal
#fi
#echo "======  docker push $IMAGE_BASE DONE======"
#
#
#echo "======  docker push $IMAGE_INFERENCE START======"
#docker push $IMAGE_INFERENCE
#retVal=$?
#if [ $retVal -ne 0 ]; then
#    echo "======  docker push $IMAGE_INFERENCE ERROR======"
#    exit $retVal
#fi
#echo "======  docker push $IMAGE_INFERENCE DONE======"
#
#
#echo "======  docker push $IMAGE_TRAIN START======"
#docker push $IMAGE_TRAIN
#retVal=$?
#if [ $retVal -ne 0 ]; then
#    echo "======  docker push $IMAGE_TRAIN ERROR======"
#    exit $retVal
#fi
#echo "======  docker push $IMAGE_TRAIN DONE======"
#
#echo ${IMAGE_BASE}
#echo ${IMAGE_INFERENCE}
#echo ${IMAGE_TRAIN}

