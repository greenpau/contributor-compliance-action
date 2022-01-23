ACTION_VERSION=`cat VERSION`
UPDATE_FILE=README.md
UPDATE_LINE=$(grep -Fn 'id: inspection' $UPDATE_FILE | cut -d":" -f1)
UPDATE_LINE=$((UPDATE_LINE+1))
USAGE_LINE="uses: greenpau/contributor-compliance-action@v$ACTION_VERSION"

sed -i '/contributor-compliance-action@/d' $UPDATE_FILE
sed -i ''"${UPDATE_LINE}"' i '"        ${USAGE_LINE}"'' $UPDATE_FILE
sed -i ''"${UPDATE_LINE}"' s/^/        /' $UPDATE_FILE
